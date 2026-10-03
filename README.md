# Carmen Wilde Fine Art — new site

Full static site hosted on GitHub Pages. Includes homepage, portfolio, original paintings, mini paintings, 54 artwork detail pages, commissions, rentals, about, contact, FAQ, shipping/returns, and terms.

## Current bridge to the existing store

The artwork catalog and detail pages are on GitHub Pages, but the **purchase button links to Carmen's existing Wix product page**. GitHub Pages has no server-side checkout. This preserves the current payment flow while the new site is reviewed. Product availability and prices were copied from the public Wix site and must be confirmed before launch. Some Wix products have a SOLD badge on the listing even though their product structured data says `InStock`, so this static catalog makes no stock claims.

The contact form composes a `mailto:` message in the visitor's email app; it does not submit or store data. Before retiring Wix, replace the checkout bridge and email-only form with a chosen payment/form provider and test end-to-end.

## Launch gate

This is a **staging site**, not an approved domain replacement. Every generated page has `noindex,nofollow` until Carmen signs off; remove that directive when the production domain is cut over. DNS still points `carmenwildefineart.com` to Wix. Do not change it yet: all 54 purchase buttons currently lead to `www.carmenwildefineart.com/product-page/...`, and they would stop working if that hostname pointed to GitHub Pages.

Before domain launch:

1. Carmen confirms ownership/permission for artwork, portrait, bio, product descriptions and publishing the work from Jack's GitHub account.
2. Carmen reviews the inventory, titles, sold status, prices, commission rates and shipping/return/policy text; the Wix structured-data `InStock` flag conflicts with visible SOLD labels.
3. Decide and implement checkout: keep Wix shop at a distinct hostname (requires Wix/domain access and end-to-end cart/payment/shipping testing) **or** move commerce to an owner-controlled provider such as Shopify. Do not collect payments in static GitHub code.
4. Decide and implement a real contact backend if an in-page form is required. The current compose-email form is honest but depends on a visitor's mail app; verify destination and receipt with Carmen, not Jack's mail infrastructure.
5. Set DNS and a Pages custom domain only after the old store remains accessible under its chosen hostname. Verify HTTPS, test an actual inquiry and a low-risk test purchase with Carmen, then remove `noindex` and add production canonical URLs and sitemap.

## Edit and rebuild

- Shared styles: `styles.css`
- Product data: `products.json`
- Static page builder: `python3 build_site.py` (uses the existing stylesheet)
- QA: start `python3 -m http.server 8766`, then run `python3 qa_site.py` (requires bs4, Pillow, Playwright and local Chrome); checks all 65 pages at three widths plus assets, internal links, menu and email-compose action.
- Catalog refresh from public Wix product sitemap: `python3 collect_products.py` (requires requests, bs4, Pillow)
- Hosting: GitHub Pages from `main` `/`, with `.nojekyll`
- `assets/silence-revised.webp` is a temporary 288 × 415 crop of Carmen's revised painting from a Messages screenshot. Replace it with the original full-resolution photo before launch; the current live Wix product artwork is not changed.

Do not point `carmenwildefineart.com` at GitHub Pages until checkout, contact handling, inventory, policy copy, and artwork permissions are approved by Carmen.
