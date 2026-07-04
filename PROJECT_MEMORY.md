# Project Memory

## 2026-07-04 - Codex

- Initialized `C:\Users\leo\astro-product-showcase` as an Astro product showcase.
- Added Astro Content Collection schema in `src/content.config.ts`.
- Added Sveltia CMS admin at `public/admin/` with GitHub backend placeholders.
- Product Markdown lives in `src/content/products/`; frontmatter stores title, brand, image, price, and stock state, while Markdown body is the product description.
- Sveltia media paths are intentionally set to `public/images/uploads` and `/images/uploads`.
- GitHub repository is `Leo-Kate/astro-product-showcase`; `public/admin/config.yml` already points Sveltia CMS at that repo.
- Before production, update `public/admin/config.yml` `site_url`, `display_url`, and OAuth proxy settings.
