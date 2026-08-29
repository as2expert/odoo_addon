from odoo import _, fields, models
from odoo.exceptions import UserError


class As2expertMessage(models.Model):
    _name = "as2expert.message"
    _description = "AS2 Message"
    _inherit = ["mail.thread"]
    _order = "create_date desc"

    name = fields.Char(compute="_compute_name", store=True)
    account_id = fields.Many2one(
        "as2expert.account", required=True, ondelete="cascade", index=True
    )
    direction = fields.Selection(
        [("outbound", "Outbound"), ("inbound", "Inbound")],
        required=True, default="outbound", tracking=True,
    )
    partner_id = fields.Many2one(
        "as2expert.partner", string="Partner",
        domain="[('account_id', '=', account_id)]",
    )
    subject = fields.Char(tracking=True)
    filename = fields.Char(string="File name")
    file = fields.Binary(string="File", attachment=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("failed", "Failed"),
            ("received", "Received"),
        ],
        default="draft", required=True, tracking=True,
    )
    message_ref = fields.Char(string="AS2 Message-ID", readonly=True, copy=False)
    message_id_api = fields.Char(string="API message id", readonly=True, copy=False, index=True)
    sent_at = fields.Datetime(readonly=True)
    received_at = fields.Datetime(readonly=True)
    error = fields.Text(readonly=True)

    _sql_constraints = [
        (
            "api_id_uniq",
            "unique(account_id, message_id_api)",
            "An inbound message is imported only once per account.",
        ),
    ]

    def _compute_name(self):
        for message in self:
            label = message.subject or message.filename or _("AS2 message")
            if message.message_ref:
                label = "%s · %s" % (label, message.message_ref)
            message.name = label

    def action_send(self):
        for message in self:
            if message.direction != "outbound":
                raise UserError(_("Only outbound messages can be sent."))
            if message.state == "sent":
                continue
            if not message.partner_id:
                raise UserError(_("Select a partner before sending."))
            if not message.file:
                raise UserError(_("Attach a file before sending."))
            content = message.file  # base64-encoded bytes
            payload = {
                "partner": int(message.partner_id.partner_ref),
                "subject": message.subject or message.filename or "AS2 document",
                "file_name": message.filename or "document.edi",
                "file_content": content.decode() if isinstance(content, bytes) else content,
            }
            try:
                data = message.account_id._api_request("/messages/send", payload)
            except Exception as exc:  # noqa: BLE001 - surface the failure on the record
                message.write({"state": "failed", "error": str(exc)})
                raise
            message.write({
                "state": "sent",
                "message_ref": (data.get("data") or {}).get("message_id") or "",
                "sent_at": fields.Datetime.now(),
                "error": False,
            })
        return True
