# Carmen Wilde Fine Art — new site

Full static site hosted on GitHub Pages. Includes homepage, portfolio, original paintings, mini paintings, 54 artwork detail pages, commissions, rentals, about, contact, FAQ, shipping/returns, and terms.

## Current bridge to the existing store

The artwork catalog and detail pages are on GitHub Pages, but the **purchase button links to Carmen's existing Wix product page**. GitHub Pages has no server-side checkout. This preserves the current payment flow while the new site is reviewed. Product availability and prices were copied from the public Wix site and must be confirmed before launch. Some Wix products have a SOLD badge on the listing even though their product structured data says `InStock`, so this static catalog makes no stock claims.

The contact form composes a `mailto:` message in the visitor's email app; it does not submit or store data. Before retiring Wix, replace the checkout bridge and email-only form with a chosen payment/form provider and test end-to-end.

## Edit and rebuild

- Shared styles: `styles.css`
- Product data: `products.json`
- Static page builder: `python3 build_site.py` (uses the existing stylesheet)
- Catalog refresh from public Wix product sitemap: `python3 collect_products.py` (requires requests, bs4, Pillow)
- Hosting: GitHub Pages from `main` `/`, with `.nojekyll`

Do not point `carmenwildefineart.com` at GitHub Pages until checkout, contact handling, inventory, policy copy, and artwork permissions are approved by Carmen.
