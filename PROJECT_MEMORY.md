# Project Memory

## 2026-07-04 - Codex

- Initialized `C:\Users\leo\astro-product-showcase` as an Astro product showcase.
- Added Astro Content Collection schema in `src/content.config.ts`.
- Added Sveltia CMS admin at `public/admin/` with GitHub backend placeholders.
- Product Markdown lives in `src/content/products/`; frontmatter stores title, brand, image, price, and stock state, while Markdown body is the product description.
- Sveltia media paths are intentionally set to `public/images/uploads` and `/images/uploads`.
- GitHub repository is `Leo-Kate/astro-product-showcase`; `public/admin/config.yml` already points Sveltia CMS at that repo.
- Cloudflare Pages project `astro-product-showcase` was created under account `61ba3d79bf14e63bd504fe379ddbfbe4`.
- Production Pages URL was initially `https://astro-product-showcase.pages.dev`.
- On 2026-07-05, custom domains `mirck.co` and `www.mirck.co` were added to the Cloudflare Pages project and both reached active status.
- DNS backup before the domain switch is stored locally at `backups/mirck.co-dns-before-pages-20260705-012138.json`.
- `mirck.co` and `www.mirck.co` DNS now use proxied CNAME records to `astro-product-showcase.pages.dev`.
- `public/admin/config.yml` `site_url` and `display_url` point to `https://mirck.co`.
- GitHub OAuth login is enabled through Cloudflare Worker `sveltia-cms-auth` at `https://sveltia-cms-auth.linfengitt.workers.dev`; callback URL is `/callback`.
- Worker secrets set outside Git: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, and `ALLOWED_DOMAINS=mirck.co,www.mirck.co`.
- `public/admin/config.yml` keeps both `oauth` and `token` auth methods so access-token login remains available as fallback.
- Added GitHub Actions workflow `.github/workflows/deploy.yml`; pushes to `main` build Astro and deploy `dist` to Cloudflare Pages using repository secrets `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`.
- Verified workflow run `28710948147` completed successfully on 2026-07-04. CMS commits to GitHub should now trigger automatic redeploys.

## 2026-07-05 - Codex

- Imported WooCommerce CSV `D:\Downloads\wc-product-export-22-6-2026-1782060704341.csv` into Astro Content Collections.
- Import generated 1,522 published simple products under `src/content/products/`.
- CSV had no regular or sale prices, so the site displays `Price on request` when `price` is absent.
- Product images are remote URLs from the export; they were not downloaded into GitHub because the CSV references 13,932 image URLs.
- Added repeatable importer `scripts/import-wc-products.py`; it accepts an optional CSV path argument and handles duplicate WooCommerce headers.
- Expanded product schema with optional `sku`, `category`, `images`, `source_id`, and `excerpt`.
- Rebuilt the frontend into a high-end watch catalogue: new dark/gold Mirck homepage, full `/products/` catalogue, and gallery-style product detail pages.
- Local verification: `npm run build` generated 1,524 pages successfully; Playwright screenshots checked desktop/mobile home, catalogue, and product detail layouts.
- Deployed the catalogue import and redesign to GitHub commit `f043c3c`; GitHub Actions run `28714947761` completed successfully and deployed to Cloudflare Pages.
- Live verification returned HTTP 200 for `https://mirck.co/`, `/products/`, `/admin/`, and a sample product detail page. Browser checks confirmed `/products/` shows `1,522 watches`, the sample product detail page renders, and `/admin/` shows the Sveltia CMS GitHub sign-in button.
