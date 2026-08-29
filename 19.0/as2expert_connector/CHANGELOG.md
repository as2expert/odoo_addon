# Changelog

## 19.0.1.0.4

- Spanish translation (`i18n/es.po`).
- Store polish: brand banner as the first gallery image, screenshots taken
  with a neutral host, and `development_status`/`maintainers` metadata.

## 19.0.1.0.3

- Screenshots now listed in the manifest `images` so they show in the Apps
  Store image gallery, not only inside the description body.

## 19.0.1.0.2

- Fix garbled symbols in the description page: emoji replaced with inline SVG
  icons, and em dash / middle dot replaced with HTML entities (ASCII-only).

## 19.0.1.0.1

- Store listing: real UI screenshots in the description page.
- Fix: message display name now stores correctly (`_compute_name` gained its
  `@api.depends`), so records no longer show as "Unnamed".

## 19.0.1.0.0

Port to Odoo 19 (same feature set as 18.0).

Odoo 19 specifics handled here:

- Security groups use the new `res.groups.privilege` model (Odoo 19 dropped
  `res.groups.category_id`) and `user_ids` instead of `users`.
- Search view group-by filters are direct children of `<search>` (Odoo 19
  removed the `expand` attribute on the `<group>` wrapper).

Carried over from 18.0:

- List views (`<list>`), `<chatter/>` element and `_compute_display_name`.
- Backend styling: app icon, SVG brand header, state/direction badges, SCSS.
- Inbound poll imports only inbound messages (`incoming`/`entrante`).

Generic AS2 file transport backed by the AS2Expert REST API: accounts,
partner sync, outbound send, and inbound via public webhook plus a 5-minute
polling fallback. No AS2 crypto in Odoo.
