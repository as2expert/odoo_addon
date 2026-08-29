from odoo import api, fields, models


class As2expertPartner(models.Model):
    _name = "as2expert.partner"
    _description = "AS2Expert Partner"
    _order = "name"

    name = fields.Char(required=True)
    account_id = fields.Many2one(
        "as2expert.account", required=True, ondelete="cascade", index=True
    )
    partner_ref = fields.Char(
        string="Partner id", required=True,
        help="The partner id used by the AS2Expert API (/messages/send 'partner').",
    )
    as2_id = fields.Char(string="AS2 ID")

    _sql_constraints = [
        (
            "ref_uniq",
            "unique(account_id, partner_ref)",
            "A partner reference must be unique per account.",
        ),
    ]

    @api.depends("name", "as2_id")
    def _compute_display_name(self):
        for partner in self:
            if partner.as2_id:
                partner.display_name = "%s (%s)" % (partner.name, partner.as2_id)
            else:
                partner.display_name = partner.name or ""
