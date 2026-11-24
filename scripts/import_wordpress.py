#!/usr/bin/env python3
"""Import public WordPress posts into this Jekyll site's Markdown archive."""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://grzegorzpawlowski.pl"
API = f"{SITE}/wp-json/wp/v2/posts?per_page=100&_embed"
EXTRA_IMAGES = {
    f"{SITE}/wp-content/uploads/2020/10/cropped-l1.png": "site-logo.png",
    f"{SITE}/wp-content/uploads/2020/12/profilowe1.png": "author.png",
}


class Element:
    def __init__(self, tag: str, attrs: dict[str, str | None] | None = None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children: list[Element | str] = []


class DocumentParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Element("root")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        element = Element(tag, dict(attrs))
        self.stack[-1].children.append(element)
        if tag not in self.VOID:
            self.stack.append(element)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack[-1].children.append(Element(tag, dict(attrs)))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def walk(element: Element):
    for child in element.children:
        if isinstance(child, Element):
            yield child
            yield from walk(child)


def raw_text(node: Element | str) -> str:
    if isinstance(node, str):
        return node
    return "".join(raw_text(child) for child in node.children)


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "static-site-import/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def download(url: str, name: str | None = None) -> str | None:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"}:
        suffix = ".jpg"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    filename = name or f"{digest}-{Path(parsed.path).stem[:60]}{suffix}"
    destination = ROOT / "assets" / "images" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "static-site-import/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                destination.write_bytes(response.read())
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"  Image skipped ({url}): {error}")
            return None
    return "/assets/images/" + filename


def category_names(post: dict) -> list[str]:
    embedded = post.get("_embedded", {}).get("wp:term", [])
    for taxonomy_group in embedded:
        categories = [item["name"] for item in taxonomy_group if item.get("taxonomy") == "category"]
        if categories:
            return categories
    return []


def image_urls(markup: str) -> list[str]:
    parser = DocumentParser()
    parser.feed(markup)
    return [element.attrs["src"] for element in walk(parser.root) if element.tag == "img" and element.attrs.get("src", "").startswith("http")]


def local_url(url: str, image_map: dict[str, str], article_slugs: set[str]) -> str:
    if url in image_map:
        return image_map[url]
    clean = url.split("#", 1)[0]
    parsed = urllib.parse.urlparse(clean)
    if parsed.hostname in {"grzegorzpawlowski.pl", "www.grzegorzpawlowski.pl"}:
        path = parsed.path or "/"
        slug = path.strip("/").split("/")[-1]
        if path.startswith("/category/"):
            return path
        if path == "/wp-admin/edit.php":
            category = urllib.parse.parse_qs(parsed.query).get("category_name", [""])[0]
            if category:
                return f"/category/{category}/"
        if slug in article_slugs:
            return f"/{slug}/"
        if path in {"/o-mnie", "/o-mnie/"}:
            return "/o-mnie/"
        if path in {"/", "/blog", "/blog/"}:
            return "/"
    return url


def inline(node: Element | str, image_map: dict[str, str], article_slugs: set[str]) -> str:
    if isinstance(node, str):
        return node.replace("\xa0", " ")
    tag = node.tag
    children = "".join(inline(child, image_map, article_slugs) for child in node.children)
    if tag in {"script", "style", "noscript"}:
        return ""
    if tag == "br":
        return "  \n"
    if tag == "img":
        src = node.attrs.get("src", "")
        alt = node.attrs.get("alt", "") or ""
        if urllib.parse.urlparse(src).hostname == "cdn.shopify.com" and src not in image_map:
            return alt
        return f"![{alt}]({local_url(src, image_map, article_slugs)})" if src else ""
    if tag == "a":
        href = node.attrs.get("href", "")
        return f"[{children}]({local_url(href, image_map, article_slugs)})" if href else children
    if tag in {"strong", "b"}:
        return f"**{children}**" if children.strip() else children
    if tag in {"em", "i"}:
        return f"*{children}*" if children.strip() else children
    if tag == "code":
        return f"`{children.strip('` ')}`" if children else ""
    if tag in {"del", "s", "strike"}:
        return f"~~{children}~~"
    if tag == "sup":
        return f"<sup>{children}</sup>"
    if tag == "sub":
        return f"<sub>{children}</sub>"
    if tag == "mark":
        return f"<mark>{children}</mark>"
    if tag == "iframe":
        src = node.attrs.get("src", "")
        return f"[Otwórz osadzony materiał]({src})" if src else ""
    return children


def list_markdown(element: Element, image_map: dict[str, str], article_slugs: set[str], depth: int = 0) -> str:
    ordered = element.tag == "ol"
    start = int(element.attrs.get("start", "1") or "1")
    lines: list[str] = []
    index = start
    for child in element.children:
        if not isinstance(child, Element) or child.tag != "li":
            continue
        marker = f"{index}. " if ordered else "- "
        index += 1
        direct: list[str] = []
        nested: list[str] = []
        for item in child.children:
            if isinstance(item, Element) and item.tag in {"ul", "ol"}:
                nested.append(list_markdown(item, image_map, article_slugs, depth + 1))
            else:
                text = inline(item, image_map, article_slugs).strip()
                if text:
                    direct.append(text)
        prefix = "  " * depth
        lines.append(prefix + marker + " ".join(direct))
        for group in nested:
            lines.extend("  " * (depth + 1) + line for line in group.splitlines())
    return "\n".join(lines)


def markdown(element: Element | str, image_map: dict[str, str], article_slugs: set[str]) -> str:
    if isinstance(element, str):
        return element.replace("\xa0", " ")
    tag = element.tag
    if tag in {"script", "style", "noscript"}:
        return ""
    if tag in {"ul", "ol"}:
        return list_markdown(element, image_map, article_slugs) + "\n\n"
    if tag == "pre":
        code = raw_text(element).strip("\n")
        language = ""
        for child in walk(element):
            classes = child.attrs.get("class", "") or ""
            match = re.search(r"(?:language|lang)-([\w+-]+)", classes)
            if match:
                language = match.group(1)
                break
        fence = "```"
        while fence in code:
            fence += "`"
        return f"{fence}{language}\n{code}\n{fence}\n\n"
    if tag == "table":
        rows = []
        for row in (item for item in walk(element) if item.tag == "tr"):
            cells = ["".join(inline(child, image_map, article_slugs) for child in cell.children).strip().replace("|", "\\|") for cell in row.children if isinstance(cell, Element) and cell.tag in {"td", "th"}]
            if cells:
                rows.append(cells)
        if rows:
            width = max(map(len, rows))
            rows = [row + [""] * (width - len(row)) for row in rows]
            first = "| " + " | ".join(rows[0]) + " |"
            divider = "| " + " | ".join("---" for _ in range(width)) + " |"
            body = ["| " + " | ".join(row) + " |" for row in rows[1:]]
            return "\n".join([first, divider, *body]) + "\n\n"
        return ""
    if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(tag[1])
        return "#" * level + " " + "".join(inline(child, image_map, article_slugs) for child in element.children).strip() + "\n\n"
    if tag == "blockquote":
        content = "".join(markdown(child, image_map, article_slugs) for child in element.children).strip()
        return "\n".join("> " + line if line else ">" for line in content.splitlines()) + "\n\n"
    if tag in {"p", "figcaption"}:
        content = "".join(inline(child, image_map, article_slugs) for child in element.children).strip()
        return content + "\n\n" if content else ""
    if tag == "figure":
        return "".join(markdown(child, image_map, article_slugs) for child in element.children)
    if tag == "hr":
        return "---\n\n"
    if tag in {"div", "section", "article", "main", "header", "footer", "span", "body", "root"}:
        return "".join(markdown(child, image_map, article_slugs) for child in element.children)
    return inline(element, image_map, article_slugs)


def plain_text(markup: str) -> str:
    parser = DocumentParser()
    parser.feed(markup)

    def extract(node: Element | str) -> str:
        if isinstance(node, str):
            return node
        if node.tag == "img":
            return node.attrs.get("alt", "") or ""
        return " ".join(extract(child) for child in node.children)

    paragraphs = [node for node in walk(parser.root) if node.tag == "p"]
    text = extract(paragraphs[0]) if paragraphs else extract(parser.root)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    posts = fetch_json(API)
    slugs = {post["slug"] for post in posts}
    image_map: dict[str, str] = {}
    all_image_urls = {url for post in posts for url in image_urls(post.get("content", {}).get("rendered", ""))}
    for post in posts:
        for media in post.get("_embedded", {}).get("wp:featuredmedia", []):
            sizes = media.get("media_details", {}).get("sizes", {})
            candidate = sizes.get("large", {}).get("source_url") or media.get("source_url")
            if candidate:
                post["_local_featured_image"] = candidate
                all_image_urls.add(candidate)

    for url in sorted(all_image_urls):
        path = download(url)
        if path:
            image_map[url] = path
    for url, filename in EXTRA_IMAGES.items():
        path = download(url, filename)
        if path:
            image_map[url] = path

    posts_dir = ROOT / "_posts"
    posts_dir.mkdir(exist_ok=True)
    imported = 0
    for post in posts:
        title = html.unescape(post["title"]["rendered"])
        content = post.get("content", {}).get("rendered", "")
        parser = DocumentParser()
        parser.feed(content)
        body = "".join(markdown(child, image_map, slugs) for child in parser.root.children)
        body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
        date = post["date"][:10]
        categories = category_names(post)
        excerpt = plain_text(content)
        if len(excerpt) > 200:
            excerpt = excerpt[:197].rsplit(" ", 1)[0] + "…"
        featured = post.get("_local_featured_image", "")
        feature_local = image_map.get(featured, "")

        front_matter = [
            "---",
            f"title: {yaml_string(title)}",
            f"date: {date}",
            f"slug: {yaml_string(post['slug'])}",
            f"permalink: /{post['slug']}/",
            f"categories: {json.dumps(categories, ensure_ascii=False)}",
            f"excerpt: {yaml_string(excerpt)}",
        ]
        if feature_local:
            front_matter.append(f"image: {yaml_string(feature_local)}")
        front_matter.extend(["layout: post", "---", "", body])
        destination = posts_dir / f"{date}-{post['slug']}.md"
        destination.write_text("\n".join(front_matter), encoding="utf-8")
        imported += 1

    print(f"Imported {imported} posts from {SITE} into {posts_dir}")
    print(f"Downloaded {len(image_map)} images into assets/images")


if __name__ == "__main__":
    main()
