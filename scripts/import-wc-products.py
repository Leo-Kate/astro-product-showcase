import csv
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = Path(r"D:\Downloads\richardmille_PERFECT_FINAL.csv")
PRODUCT_DIR = ROOT / "src" / "content" / "products"
GENERATED_DIR = ROOT / "src" / "generated"
IMAGE_MAP_FILE = GENERATED_DIR / "image-map.ts"


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


def proxied_image_path(url):
    if not url or url.startswith("/"):
        return url

    clean_url = url.split("?", 1)[0]
    extension = Path(clean_url).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}:
        extension = ".jpg"

    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:24]
    return f"/cdn-image/{digest}{extension}"


def get_field(row, *names):
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip():
            return value
    return ""


def parse_price(value):
    cleaned = re.sub(r"[^0-9.]", "", str(value or ""))
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


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
        if truthy(get_field(row, "已发布", "Published"))
        and (get_field(row, "类型", "Type") or "simple") == "simple"
    ]

    if PRODUCT_DIR.exists():
        shutil.rmtree(PRODUCT_DIR)

    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    used_slugs = {}
    image_map = {}

    for row in rows:
        title = get_field(row, "名称", "Name").strip()
        category = get_field(row, "分类", "Categories").strip()
        category_root = category.split(">")[0].strip() if category else ""
        brand = (get_field(row, "品牌") or category_root or "Mirck Atelier").strip()
        sku = get_field(row, "SKU").strip()
        source_images = split_images(get_field(row, "图片", "Images"))
        images = []
        for source_image in source_images:
            proxied = proxied_image_path(source_image)
            images.append(proxied)
            image_map[proxied.removeprefix("/cdn-image/")] = source_image
        image = images[0] if images else "/images/uploads/atlas-modular-pack.svg"
        excerpt = strip_tags(get_field(row, "简短描述", "Short description"))[:280]
        body = clean_description(get_field(row, "描述", "Description") or excerpt)
        price = parse_price(get_field(row, "常规价格", "Regular price"))

        base_slug = slugify(f"{brand}-{sku or get_field(row, 'ID')}-{title}")
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
            "price": price,
            "in_stock": truthy(get_field(row, "有货？", "In stock?")),
            "source_id": get_field(row, "ID").strip() or None,
            "excerpt": excerpt or None,
        }

        (PRODUCT_DIR / f"{slug}.md").write_text(
            f"{frontmatter(data)}\n\n{body}\n",
            encoding="utf-8",
            newline="\n",
        )

    IMAGE_MAP_FILE.write_text(
        "export const imageMap: Record<string, string> = "
        + json.dumps(dict(sorted(image_map.items())), ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"Imported {len(rows)} products into {PRODUCT_DIR}")
    print(f"Mapped {len(image_map)} remote images through /cdn-image/")


if __name__ == "__main__":
    main()
