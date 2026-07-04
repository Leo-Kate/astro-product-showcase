# Astro Product Showcase

Commercial product showcase built with Astro Content Collections and Sveltia CMS.

## Project Structure

Important files:

```text
/
├── public/
│   ├── admin/
│   │   ├── config.yml
│   │   └── index.html
│   └── images/uploads/
├── src/
│   ├── content/products/
│   ├── content.config.ts
│   └── pages/
│       ├── index.astro
│       └── products/[slug].astro
└── package.json
```

Product data lives in `src/content/products/*.md`. Structured fields stay in frontmatter:

```yaml
---
title: Atlas Modular Pack
brand: Northline Goods
image: /images/uploads/atlas-modular-pack.svg
price: 189
in_stock: true
---
```

The Markdown body is the product description edited in Sveltia CMS.

## CMS Setup

The Sveltia CMS admin is available at `/admin/`.

Before deployment, edit `public/admin/config.yml`:

- Confirm `repo: Leo-Kate/astro-product-showcase` matches your GitHub repository.
- Replace `https://example.com` with the production domain.
- Keep `media_folder: public/images/uploads` and `public_folder: /images/uploads`.

For GitHub OAuth, use a deployed OAuth proxy such as Decap CMS OAuth Server on Cloudflare Workers, then add its endpoint to the Sveltia backend config. Token login is also enabled for early testing.

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
