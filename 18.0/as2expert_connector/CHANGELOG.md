# Changelog

## 18.0.1.0.5

- Screenshots now listed in the manifest `images` so they show in the Apps
  Store image gallery, not only inside the description body.

## 18.0.1.0.4

- Fix garbled symbols in the description page: emoji replaced with inline SVG
  icons, and em dash / middle dot replaced with HTML entities (ASCII-only).

## 18.0.1.0.3

- Store listing: real UI screenshots in the description page.
- Fix: message display name now stores correctly (`_compute_name` gained its
  `@api.depends`), so records no longer show as "Unnamed".

## 18.0.1.0.2

- Backend styling: app icon, brand header with SVG logo, coloured state and
  direction badges in the message list, and a light SCSS asset bundle.

## 18.0.1.0.1

- Inbound poll now imports only inbound messages (`incoming`/`entrante`);
  the `/messages` endpoint returns both directions.

## 18.0.1.0.0

Port to Odoo 18.

- List views use the `<list>` element and `list,form` view modes.
- Chatter uses the `<chatter/>` element.
- Partner display name via `_compute_display_name` (Odoo 18 drops `name_get`).

Functionally identical to the 17.0 release:

- AS2Expert **Account** model: API base URL + token, station scope, poll batch
  size, and a per-account webhook URL/secret. Actions: *Test connection*,
  *Sync partners*, *Poll inbound now*.
- **Partner** model synced from the AS2Expert station.
- **Message** model (outbound send + inbound receive) with the file stored as a
  downloadable attachment; inherits `mail.thread`.
- Public **webhook** controller (`/as2expert/webhook/<token>`) with optional
  HMAC-SHA256 body verification, acting only as a trigger for the inbound poll.
- Scheduled action polling inbound messages every 5 minutes as a fallback.
- Security groups *AS2 User* / *AS2 Administrator* and per-model access rules.
