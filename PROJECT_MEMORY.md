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
