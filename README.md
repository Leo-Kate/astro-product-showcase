# Astro Product Showcase

Commercial Richard Mille product showcase built with Astro Content Collections and Sveltia CMS.

## Project Structure

Important files:

```text
/
├── public/
│   ├── admin/
│   │   ├── config.yml
│   │   └── index.html
│   └── images/uploads/
├── functions/
│   ├── admin/[[path]].ts
│   └── cdn-image/[image].ts
├── src/
│   ├── content/products/
│   ├── generated/image-map.ts
│   ├── lib/catalog.ts
│   ├── content.config.ts
│   └── pages/
│       ├── collections/[collection].astro
│       ├── index.astro
│       └── products/[slug].astro
└── package.json
```

Product data lives in `src/content/products/*.md`. Structured fields stay in frontmatter:

```yaml
---
title: Richard Mille RM 67-02 McLaren Lando Norris
brand: Richard Mille
sku: RM-F859FE4D
category: Richard Mille > RM 67-02
image: /cdn-image/example.webp
price: 10000
in_stock: true
---
```

The Markdown body is the product description edited in Sveltia CMS.

## Import Products

WooCommerce product exports can be imported with:

```sh
python scripts/import-wc-products.py "D:\Downloads\richardmille_PERFECT_FINAL.csv"
```

The importer rewrites remote product images through `/cdn-image/...` and writes the source URL map to `src/generated/image-map.ts`. Cloudflare Pages Functions fetch and cache those images at the edge, so the public pages do not expose the original third-party image URLs directly.

## CMS Setup

The Sveltia CMS admin is available at `/admin/`, protected by Cloudflare Pages Basic Auth before the GitHub login screen.

Before deployment, edit `public/admin/config.yml`:

- Confirm `repo: Leo-Kate/astro-product-showcase` matches your GitHub repository.
- Production domain is `https://mirck.co`.
- Keep `media_folder: public/images/uploads` and `public_folder: /images/uploads`.

The CMS supports GitHub OAuth through `https://sveltia-cms-auth.linfengitt.workers.dev` and keeps access-token login as a fallback.

Set these Cloudflare Pages production secrets before deploying admin protection:

- `ADMIN_USER`
- `ADMIN_PASSWORD`

WhatsApp is configured in `src/lib/catalog.ts`.

## Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |
