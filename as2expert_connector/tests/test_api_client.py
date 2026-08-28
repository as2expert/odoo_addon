from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class FakeResponse:
    def __init__(self, payload, status_code=200, is_json=True):
        self._payload = payload
        self.status_code = status_code
        self._is_json = is_json

    def json(self):
        if not self._is_json:
            raise ValueError("not json")
        return self._payload


class TestApiClient(TransactionCase):
    def setUp(self):
        super().setUp()
        self.account = self.env["as2expert.account"].create({
            "name": "Test",
            "base_url": "https://example.test/api/v1",
            "token": "secret-token",
        })

    def _patch(self, response):
        return patch(
            "odoo.addons.as2expert_connector.models.as2expert_account.requests.post",
            return_value=response,
        )

    def test_success_returns_payload(self):
        payload = {"status": "success", "data": [{"id": 1}], "total": 1}
        with self._patch(FakeResponse(payload)) as mocked:
            data = self.account._api_request("/stations", {})
        self.assertEqual(data, payload)
        # Bearer token is sent in the Authorization header.
        _, kwargs = mocked.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer secret-token")

    def test_logical_failure_raises(self):
        payload = {"status": "error", "msg": "nope"}
        with self._patch(FakeResponse(payload)):
            with self.assertRaises(UserError):
                self.account._api_request("/stations", {})

    def test_http_401_raises(self):
        with self._patch(FakeResponse({}, status_code=401)):
            with self.assertRaises(UserError):
                self.account._api_request("/stations", {})

    def test_non_json_raises(self):
        with self._patch(FakeResponse(None, is_json=False)):
            with self.assertRaises(UserError):
                self.account._api_request("/stations", {})

    def test_webhook_url_uses_token(self):
        self.assertTrue(self.account.webhook_token)
        self.assertIn(self.account.webhook_token, self.account.webhook_url)
