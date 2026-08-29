import hashlib
import hmac
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class As2expertWebhook(http.Controller):
    """Public endpoint AS2Expert calls when a message event happens.

    The webhook is only a trigger: it verifies the caller (unguessable token in
    the URL, plus an optional HMAC signature of the body) and then runs the
    inbound poll, which pulls new messages from the well-defined REST API. That
    keeps the receiver robust to the exact webhook payload shape.
    """

    def _json(self, payload, status=200):
        return request.make_response(
            json.dumps(payload),
            headers=[("Content-Type", "application/json")],
            status=status,
        )

    @http.route(
        ["/as2expert/webhook/<string:token>"],
        type="http", auth="public", methods=["POST"], csrf=False, save_session=False,
    )
    def webhook(self, token, **kwargs):
        account = request.env["as2expert.account"].sudo().search(
            [("webhook_token", "=", token), ("active", "=", True)], limit=1
        )
        if not account:
            return self._json({"status": "error", "error": "unknown token"}, status=404)

        raw_body = request.httprequest.get_data() or b""
        if account.webhook_secret:
            provided = (
                request.httprequest.headers.get("X-AS2Expert-Signature")
                or request.httprequest.headers.get("X-Signature")
                or ""
            ).strip()
            expected = hmac.new(
                account.webhook_secret.encode("utf-8"), raw_body, hashlib.sha256
            ).hexdigest()
            candidates = (expected, "sha256=" + expected)
            if not provided or not any(hmac.compare_digest(provided, c) for c in candidates):
                _logger.warning("AS2Expert webhook signature mismatch for account %s", account.id)
                return self._json({"status": "error", "error": "invalid signature"}, status=401)

        try:
            imported = account.poll_inbound()
        except Exception:  # noqa: BLE001 - never leak internals to the caller
            _logger.exception("AS2Expert webhook poll failed for account %s", account.id)
            return self._json({"status": "error", "error": "poll failed"}, status=500)

        return self._json({"status": "ok", "imported": imported})
