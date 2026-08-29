# Changelog

## 17.0.1.0.2

- Backend styling: app icon, brand header with SVG logo, coloured state and
  direction badges in the message list, and a light SCSS asset bundle.

## 17.0.1.0.1

- Inbound poll now imports only inbound messages (`incoming`/`entrante`);
  the `/messages` endpoint returns both directions.

## 17.0.1.0.0

Initial release.

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
