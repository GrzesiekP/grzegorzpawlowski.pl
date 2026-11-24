#!/usr/bin/env python3
"""Check local links and images in a Jekyll build (no third-party packages)."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag in {"a", "link"} and "href" in attributes:
            self.urls.append(attributes["href"])
        if tag in {"img", "script", "source"} and "src" in attributes:
            self.urls.append(attributes["src"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="Directory containing the built site")
    args = parser.parse_args()
    root = args.site.resolve()
    pages = {}
    for file in root.rglob("*.html"):
        document = References()
        document.feed(file.read_text(encoding="utf-8"))
        pages[file] = document
    if not pages:
        parser.error(f"No HTML pages found in {root}")

    errors = set()
    checked = 0
    for prefix in ("/", "/grzegorzpawlowski.pl/"):
        for file, document in pages.items():
            path = file.relative_to(root).as_posix()
            route = path.removesuffix("index.html") if path.endswith("index.html") else path
            base = "https://preview.invalid" + prefix + route
            for ref in document.urls:
                parts = urlsplit(ref)
                if parts.scheme or parts.netloc:
                    continue  # External links are checked separately, not during offline validation.
                target = urlsplit(urljoin(base, ref))
                target_path = unquote(target.path)
                if not target_path.startswith(prefix):
                    errors.add(f"{path}: {ref} escapes the deployment path {prefix}")
                    continue
                local = root / target_path[len(prefix):]
                if local.is_dir():
                    local /= "index.html"
                if not local.is_file():
                    errors.add(f"{path}: missing target for {ref}")
                elif target.fragment and local in pages and unquote(target.fragment) not in pages[local].ids:
                    errors.add(f"{path}: missing anchor in {ref}")
                checked += 1

    for error in sorted(errors):
        print(error)
    print(f"{len(pages)} pages, {checked} local references (root + project path), {len(errors)} errors")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
