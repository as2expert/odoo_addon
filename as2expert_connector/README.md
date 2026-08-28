# AS2Expert Connector (Odoo 17)

Send and receive files over **AS2** from inside Odoo, using the
[AS2Expert](https://www.as2expert.com) cloud platform. Odoo never runs an AS2
server or touches certificates: AS2Expert handles signing, encryption, MDNs and
partner connectivity. This addon only exchanges files through the documented
AS2Expert REST API and reacts to its webhooks.

It is deliberately **transport-generic** — it moves *files* (EDIFACT, X12, XML,
PDF, anything) and does not parse or map document content. Pair it with your own
EDI mapping, or with AS2Expert's built-in EDIFACT tooling.

## What you get

- **Accounts** — one record per AS2Expert token (API base URL + token). Multiple
  accounts/stations are supported.
- **Partners** — synced from your AS2Expert station with one click.
- **Outbound** — attach a file, pick a partner, press *Send over AS2*.
- **Inbound** — received messages land as records with the file attached,
  through a real-time **webhook** plus a **scheduled poll** fallback (every 5
  minutes) so nothing is missed if a webhook is dropped.

## Requirements

- Odoo **17.0**.
- Python `requests` (bundled with Odoo).
- An AS2Expert account with an API token (AS2Expert console → API tokens).

## Install

1. Copy `as2expert_connector/` into an Odoo addons path (or symlink it):
   ```
   cp -r odoo/as2expert_connector /path/to/odoo/addons/
   ```
2. Restart Odoo and **Update Apps List** (developer mode).
3. Install **AS2Expert Connector** from *Apps*.

## Configure

1. **AS2Expert ▸ Configuration ▸ Accounts ▸ New.**
   - *API base URL*: `https://b2b.as2expert.com/api/v1` (default).
   - *API token*: paste the Bearer token from the AS2Expert console.
   - *Station id* (optional): scope polling/partner sync to one station.
   - *Poll batch size*: max inbound messages fetched per poll.
2. Press **Test connection** — it calls `/stations` and reports how many stations
   the token can see.
3. Press **Sync partners** — imports partners into *AS2Expert ▸ Partners*.
4. **Webhook (real-time inbound):**
   - Copy the read-only **Webhook URL** shown on the account
     (`https://<your-odoo>/as2expert/webhook/<token>`).
   - Register it as the partner/event webhook in the AS2Expert console.
   - Optional but recommended: set a **Webhook secret** here and configure the
     same secret in AS2Expert. When set, the controller verifies an
     HMAC-SHA256 signature of the request body
     (`X-AS2Expert-Signature` / `X-Signature`, bare hex or `sha256=` prefix)
     before doing anything.
   - Your Odoo must be reachable from AS2Expert over HTTPS for webhooks; if it
     is not, the scheduled poll still delivers inbound messages.

The webhook is only a **trigger**: it authenticates the caller and then runs the
same inbound poll used by the cron, which pulls messages from the REST API. This
makes inbound delivery robust to the exact webhook payload shape and idempotent
(messages are de-duplicated by their API id).

## Send a file

**AS2Expert ▸ Messages ▸ New** (or the *Messages* stat button on an account):

1. Pick the **account** and **partner**.
2. Upload the **file** and set a **subject** (optional).
3. Press **Send over AS2**. On success the record shows *Sent* and the returned
   AS2 Message-ID; on failure it shows *Failed* with the error text.

## Scheduled poll

*Settings ▸ Technical ▸ Automation ▸ Scheduled Actions ▸
`AS2Expert: poll inbound messages`* runs every 5 minutes across all active
accounts. Adjust the interval there.

## Security model

- Two groups: **AS2Expert / User** (send, view, manage partners & messages) and
  **AS2Expert / Manager** (also manages accounts and tokens).
- The webhook route is `auth="public"` (AS2Expert is unauthenticated to Odoo);
  it is protected by the unguessable per-account token in the URL and the
  optional HMAC secret. Tokens/secrets are stored on the account record and the
  token/secret fields are masked in the form.

## API endpoints used

`POST` to the AS2Expert REST API v1, all expecting `{"status": "success", ...}`:

| Purpose            | Path                 |
|--------------------|----------------------|
| Test / list stations | `/stations`        |
| Sync partners      | `/partners`          |
| List inbound       | `/messages`          |
| Message detail     | `/messages/detail`   |
| Download content   | `/messages/download` |
| Send               | `/messages/send`     |

## Tests

Unit tests (with `requests` mocked, no live API needed) live in `tests/`:

```
odoo-bin -d <db> -i as2expert_connector --test-enable --stop-after-init
```

## Limitations

- Transport only — no EDI parsing/validation in Odoo.
- Field names read from API responses tolerate both English and legacy keys
  (`file_name`/`asunto`, `content_b64`/`contenido_base64`, …); if your tenant
  returns different keys, adjust `_import_inbound` / `action_sync_partners`.

## License

[LGPL-3](LICENSE). Contributions welcome — open an issue or PR on GitHub.
