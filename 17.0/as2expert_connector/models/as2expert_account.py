import logging
import secrets

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://b2b.as2expert.com/api/v1"


class As2expertAccount(models.Model):
    _name = "as2expert.account"
    _description = "AS2Expert Account"
    _order = "name"

    name = fields.Char(required=True, default="AS2Expert")
    active = fields.Boolean(default=True)
    base_url = fields.Char(
        string="API base URL",
        required=True,
        default=DEFAULT_BASE_URL,
        help="AS2Expert REST API base, e.g. https://b2b.as2expert.com/api/v1",
    )
    token = fields.Char(
        string="API token",
        required=True,
        help="Bearer token issued from the AS2Expert console. Stored server-side.",
    )
    timeout = fields.Integer(default=30, help="HTTP timeout per request, in seconds.")

    station_ref = fields.Char(
        string="Station id",
        help="Optional AS2Expert station id to scope message polling to one station.",
    )
    inbound_folder = fields.Char(
        string="Inbound folder",
        help="Optional folder name/key the API uses for received messages "
        "(passed as the 'folder' filter). Leave empty to poll all folders.",
    )
    poll_limit = fields.Integer(
        string="Poll batch size", default=50,
        help="Maximum inbound messages fetched per poll.",
    )

    webhook_token = fields.Char(
        string="Webhook token",
        readonly=True,
        copy=False,
        default=lambda self: secrets.token_urlsafe(24),
        help="Unguessable token that forms the public webhook URL for this account.",
    )
    webhook_secret = fields.Char(
        string="Webhook secret",
        help="Optional shared secret. If set and AS2Expert signs the webhook body "
        "(HMAC-SHA256), the signature is verified before the poll is triggered.",
    )
    webhook_url = fields.Char(
        string="Webhook URL", compute="_compute_webhook_url",
        help="Register this URL as the partner webhook in AS2Expert.",
    )

    message_count = fields.Integer(compute="_compute_counts")
    partner_count = fields.Integer(compute="_compute_counts")

    _sql_constraints = [
        ("webhook_token_uniq", "unique(webhook_token)", "The webhook token must be unique."),
    ]

    def _compute_webhook_url(self):
        base = self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        for account in self:
            account.webhook_url = (
                "%s/as2expert/webhook/%s" % (base.rstrip("/"), account.webhook_token)
                if account.webhook_token else False
            )

    def _compute_counts(self):
        Message = self.env["as2expert.message"]
        Partner = self.env["as2expert.partner"]
        for account in self:
            account.message_count = Message.search_count([("account_id", "=", account.id)])
            account.partner_count = Partner.search_count([("account_id", "=", account.id)])

    # ------------------------------------------------------------------
    # REST client
    # ------------------------------------------------------------------
    def _api_request(self, path, payload=None):
        """POST to an AS2Expert API endpoint and return the parsed JSON.

        Raises UserError on transport errors, non-JSON bodies, or a logical
        failure (``status`` != ``"success"``) even when the HTTP code is 200.
        """
        self.ensure_one()
        if not self.token:
            raise UserError(_("No API token configured for account '%s'.") % self.name)
        url = (self.base_url or DEFAULT_BASE_URL).rstrip("/") + path
        headers = {
            "Authorization": "Bearer %s" % self.token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            response = requests.post(
                url, json=payload or {}, headers=headers, timeout=self.timeout or 30
            )
        except requests.RequestException as exc:
            raise UserError(_("AS2Expert API connection error: %s") % exc)

        if response.status_code == 401:
            raise UserError(_("AS2Expert API rejected the token (HTTP 401)."))
        if response.status_code == 403:
            raise UserError(_("AS2Expert API: the token lacks the required scope (HTTP 403)."))
        try:
            data = response.json()
        except ValueError:
            raise UserError(
                _("AS2Expert API returned a non-JSON response (HTTP %s).")
                % response.status_code
            )
        if not isinstance(data, dict) or data.get("status") != "success":
            message = ""
            if isinstance(data, dict):
                message = data.get("msg") or data.get("message") or data.get("status") or ""
            raise UserError(_("AS2Expert API error: %s") % (message or response.status_code))
        return data

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_test_connection(self):
        self.ensure_one()
        data = self._api_request("/stations", {})
        total = data.get("total")
        if total is None:
            total = len(data.get("data") or [])
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "title": _("AS2Expert"),
                "message": _("Connection OK. %s station(s) visible to this token.") % total,
                "sticky": False,
            },
        }

    def action_sync_partners(self):
        Partner = self.env["as2expert.partner"]
        for account in self:
            payload = {}
            if account.station_ref:
                payload["station"] = int(account.station_ref)
            data = account._api_request("/partners", payload)
            for item in data.get("data") or []:
                ref = str(item.get("id") or "")
                if not ref:
                    continue
                vals = {
                    "account_id": account.id,
                    "partner_ref": ref,
                    "name": item.get("name") or item.get("nombre") or ref,
                    "as2_id": item.get("as2_id") or item.get("as2id") or "",
                }
                existing = Partner.search(
                    [("account_id", "=", account.id), ("partner_ref", "=", ref)], limit=1
                )
                if existing:
                    existing.write(vals)
                else:
                    Partner.create(vals)
        return True

    def action_regenerate_webhook_token(self):
        for account in self:
            account.webhook_token = secrets.token_urlsafe(24)
        return True

    def action_view_messages(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("AS2 Messages"),
            "res_model": "as2expert.message",
            "view_mode": "tree,form",
            "domain": [("account_id", "=", self.id)],
            "context": {"default_account_id": self.id},
        }

    # ------------------------------------------------------------------
    # Inbound polling (source of truth; webhook only triggers it)
    # ------------------------------------------------------------------
    def poll_inbound(self):
        Message = self.env["as2expert.message"]
        imported = 0
        for account in self:
            payload = {"limit": account.poll_limit or 50}
            if account.station_ref:
                payload["station"] = int(account.station_ref)
            if account.inbound_folder:
                payload["folder"] = account.inbound_folder
            data = account._api_request("/messages", payload)
            for item in data.get("data") or []:
                api_id = str(item.get("id") or "")
                if not api_id:
                    continue
                if Message.search_count(
                    [("account_id", "=", account.id), ("message_id_api", "=", api_id)]
                ):
                    continue
                account._import_inbound(item)
                imported += 1
        return imported

    def _import_inbound(self, item):
        self.ensure_one()
        api_id = str(item.get("id"))
        detail = self._api_request("/messages/detail", {"id": api_id}).get("data") or {}
        download = self._api_request("/messages/download", {"id": api_id}).get("data") or {}
        content_b64 = download.get("content_b64") or download.get("contenido_base64")
        filename = (
            detail.get("file_name")
            or detail.get("asunto")
            or item.get("asunto")
            or ("as2-%s.bin" % api_id)
        )
        message = self.env["as2expert.message"].create({
            "account_id": self.id,
            "direction": "inbound",
            "message_id_api": api_id,
            "message_ref": detail.get("message_id") or detail.get("idmensaje") or "",
            "subject": detail.get("subject") or detail.get("asunto") or item.get("asunto") or "",
            "filename": filename,
            "file": content_b64 or False,
            "state": "received",
            "received_at": fields.Datetime.now(),
        })
        return message

    @api.model
    def _cron_poll_inbound(self):
        for account in self.search([("active", "=", True)]):
            try:
                account.poll_inbound()
            except Exception:  # noqa: BLE001 - one account must not stop the others
                _logger.exception("AS2Expert polling failed for account %s", account.display_name)
        return True
