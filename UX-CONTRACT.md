# UX contract
Source: PRODUCT.md. Local persistence only; no accounts, external writes, payment, or destructive actions. Locale en-GB, timestamps shown in Asia/Jakarta and labeled WIB. Browser photos are ephemeral. Intake metadata persists only on Save; failure leaves entered values available. Records stored per key to avoid cross-tab overwrites. No edit/delete flow in this release. History is newest first, 10 per page. Filters are transient browser-local to avoid exposing intake state in shared URLs.
| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
|---|---|---|---|---|
| Select/Listbox | native select | DESIGN.md | material and history filters | static checks |
| Form | intake form in app.js | PRODUCT.md | save reviewed intake | validation tests |
| Scrollbar | global style.css | DESIGN.md | global | static audit |
| Toast | status() in app.js | UX-CONTRACT.md | success and error | live region check |
| CRUD | local record service in app.js | PRODUCT.md | create/read/export | functional tests |
Flow: select image → preview → analyze (busy, duplicate blocked) → review prediction → select actual material and optional weight → Save → history, success status. Failed inference retains image and offers retry. Changing image invalidates previous prediction. Low top score <0.65 prompts manual review; this is a heuristic, not calibrated confidence. Manual review is always required.
