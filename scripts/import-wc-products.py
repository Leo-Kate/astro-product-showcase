import csv
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = Path(r"D:\Downloads\wc-product-export-22-6-2026-1782060704341.csv")
PRODUCT_DIR = ROOT / "src" / "content" / "products"


def make_unique_headers(headers):
    seen = {}
    result = []

    for header in headers:
        seen[header] = seen.get(header, 0) + 1
        result.append(header if seen[header] == 1 else f"{header}_{seen[header]}")

    return result


def truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def slugify(value):
    value = html.unescape(value or "").lower()
    value = re.sub(r"['’]", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "product"


def strip_tags(value):
    value = html.unescape(value or "")
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def clean_description(value):
    value = html.unescape(value or "").replace("\\n", "\n").replace("\r\n", "\n")
    value = re.sub(r"<table[\s\S]*?</table>", "", value, flags=re.I)
    value = re.sub(r"\sstyle=\"[^\"]*\"", "", value, flags=re.I)
    value = re.sub(r"</?font[^>]*>", "", value, flags=re.I)
    value = re.sub(r"<p>\s*</p>", "", value, flags=re.I)
    value = re.sub(r"\n{3,}", "\n\n", value).strip()
    return value or "Contact us for full specifications and availability."


def split_images(value):
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def frontmatter(data):
    lines = ["---"]

    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = json.dumps(value, ensure_ascii=False)
        lines.append(f"{key}: {rendered}")

    lines.append("---")
    return "\n".join(lines)


def load_rows(csv_path):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        headers = make_unique_headers(next(reader))

        for row in reader:
            yield dict(zip(headers, row))


def main():
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV_PATH

    rows = [
        row
        for row in load_rows(csv_path)
        if truthy(row.get("已发布", "")) and (row.get("类型") or "simple") == "simple"
    ]

    if PRODUCT_DIR.exists():
        shutil.rmtree(PRODUCT_DIR)

    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)

    used_slugs = {}

    for row in rows:
        title = (row.get("名称") or "").strip()
        category = (row.get("分类") or "").strip()
        category_root = category.split(">")[0].strip() if category else ""
        brand = (row.get("品牌") or category_root or "Mirck Atelier").strip()
        sku = (row.get("SKU") or "").strip()
        images = split_images(row.get("图片"))
        image = images[0] if images else "/images/uploads/atlas-modular-pack.svg"
        excerpt = strip_tags(row.get("简短描述"))[:280]
        body = clean_description(row.get("描述"))

        base_slug = slugify(f"{brand}-{sku or row.get('ID')}-{title}")
        count = used_slugs.get(base_slug, 0)
        used_slugs[base_slug] = count + 1
        slug = base_slug if count == 0 else f"{base_slug}-{count + 1}"

        data = {
            "title": title,
            "brand": brand,
            "sku": sku or None,
            "category": category or None,
            "image": image,
            "images": images[:12],
            "in_stock": truthy(row.get("有货？", "")),
            "source_id": (row.get("ID") or "").strip() or None,
            "excerpt": excerpt or None,
        }

        (PRODUCT_DIR / f"{slug}.md").write_text(
            f"{frontmatter(data)}\n\n{body}\n",
            encoding="utf-8",
            newline="\n",
        )

    print(f"Imported {len(rows)} products into {PRODUCT_DIR}")


if __name__ == "__main__":
    main()
