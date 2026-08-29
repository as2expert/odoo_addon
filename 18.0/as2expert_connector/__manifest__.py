{
    "name": "AS2Expert Connector",
    "version": "18.0.1.0.1",
    "summary": "Send and receive files over AS2 through AS2Expert's REST API and webhooks",
    "description": """
AS2Expert Connector
===================

Exchange business documents over AS2 without operating an AS2 server, using the
AS2Expert cloud platform (https://www.as2expert.com).

This is a generic AS2 mailbox inside Odoo:

* Configure one or more AS2Expert accounts (API base URL + token).
* Sync the partners defined in your AS2Expert station.
* Send any file to a partner over AS2 (signed and encrypted by AS2Expert).
* Receive inbound messages as Odoo attachments, via a webhook (real time) and a
  scheduled polling fallback.

The connector never handles AS2 crypto itself: AS2Expert provides the endpoint,
certificates, signing, encryption and MDNs. Odoo only exchanges files through
the documented REST API.
""",
    "author": "AS2Expert",
    "website": "https://www.as2expert.com",
    "support": "contact@as2expert.com",
    "category": "Inventory/EDI",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/as2expert_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/as2expert_account_views.xml",
        "views/as2expert_partner_views.xml",
        "views/as2expert_message_views.xml",
        "views/as2expert_menus.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": True,
    "installable": True,
}
