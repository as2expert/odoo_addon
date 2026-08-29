# AS2Expert Odoo Connector

[![Odoo](https://img.shields.io/badge/Odoo-17.0%20%7C%2018.0-875A7B)](https://www.odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue)](LICENSE)

Send and receive files over **AS2** straight from Odoo — no AS2 server to run,
no certificates to babysit. This repository holds the `as2expert_connector`
addon, which turns Odoo into a generic AS2 mailbox backed by the
[AS2Expert](https://www.as2expert.com) cloud platform.

The addon is kept **one folder per Odoo version** so each release stays pinned
and easy to track:

| Odoo | Folder |
|------|--------|
| 18.0 | [`18.0/as2expert_connector`](18.0/as2expert_connector) |
| 17.0 | [`17.0/as2expert_connector`](17.0/as2expert_connector) |

AS2Expert does the hard part — signing, encryption, MDNs, certificate management
and partner connectivity. Odoo only exchanges **files** through the documented
REST API and reacts to webhooks. The addon is deliberately **transport-generic**:
it moves EDIFACT, X12, XML, PDF or any payload and does not parse content, so you
keep your document mapping wherever it already lives.

> New to the platform? Read [**AS2EXPERT.md**](AS2EXPERT.md) for a short overview
> of what AS2Expert is and why it exists.

## Features

- **Accounts** — one record per AS2Expert token (API base URL + token); multiple
  accounts/stations supported.
- **Partners** — synced from your AS2Expert station with one click.
- **Outbound** — attach a file, pick a partner, press *Send over AS2*.
- **Inbound** — messages arrive with the file attached, via a real-time
  **webhook** plus a **5-minute polling fallback**, de-duplicated by API id.
- **Guarded webhook** — unguessable per-account token in the URL and optional
  HMAC-SHA256 verification of the request body.
- **Security** — *AS2 User* / *AS2 Administrator* groups and per-model access
  rules.

## Requirements

- Odoo **17.0** or **18.0** (Community or Enterprise)
- An AS2Expert account with an API token
- Python `requests` (bundled with Odoo)

## Install

Pick the folder that matches your Odoo version, e.g. for Odoo 18:

```bash
# copy (or symlink) the addon into an Odoo addons path
cp -r 18.0/as2expert_connector /path/to/odoo/addons/
```

Restart Odoo, **Update Apps List** (developer mode), then install
**AS2Expert Connector** from *Apps*.

## Configure

1. **AS2Expert ▸ Configuration ▸ Accounts ▸ New** — set the API base URL
   (`https://b2b.as2expert.com/api/v1`) and your token.
2. Press **Test connection**, then **Sync partners**.
3. Copy the account's **Webhook URL** and register it in the AS2Expert console.
   Optionally set a **Webhook secret** on both sides for HMAC verification.

Full details, including the send flow and the scheduled poll, are in the
addon README ([18.0](18.0/as2expert_connector/README.md) ·
[17.0](17.0/as2expert_connector/README.md)).

## Tests

Unit tests mock `requests`, so no live API is needed. Point the addons path at
the version folder, e.g.:

```bash
odoo-bin --addons-path=18.0 -d <db> -i as2expert_connector \
  --test-enable --stop-after-init
```

CI runs the suite against both 17.0 and 18.0 on every push.

## Contributing

Issues and pull requests are welcome. Please keep the addon transport-generic
(no document parsing) and run the test suite before submitting.

## License

[LGPL-3](LICENSE).
