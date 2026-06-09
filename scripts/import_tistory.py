#!/usr/bin/env python3
"""Import public Tistory posts into this Jekyll repository.

The importer intentionally uses only dependencies already present in the
project environment: requests, BeautifulSoup, and PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import mimetypes
import posixpath
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag


BASE_URL = "https://upright-wing.tistory.com"
POSTS_DIR = Path("_posts")
IMAGES_DIR = Path("assets/img/tistory")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)
SKIP_CLASSES = {
    "container_postbtn",
    "another_category",
    "revenue_unit_wrap",
    "adsbygoogle",
}


@dataclass(frozen=True)
class PostSummary:
    post_id: str
    url: str
    title: str
    category: str
    listed_date: str


class HtmlToMarkdown:
    def convert(self, root: Tag) -> str:
        blocks = [self._convert_node(child, block=True).strip() for child in root.children]
        markdown = "\n\n".join(block for block in blocks if block)
        markdown = markdown.replace("\xa0", " ")
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        return markdown.strip() + "\n"

    def _convert_node(self, node, block: bool = False) -> str:
        if isinstance(node, NavigableString):
            return str(node)
        if not isinstance(node, Tag):
            return ""
        if self._should_skip(node):
            return ""

        name = node.name.lower()
        if name in {"script", "style", "noscript"}:
            return ""
        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            return f"{'#' * level} {self._inline(node).strip()}"
        if name == "p":
            return self._inline(node).strip()
        if name == "br":
            return "\n"
        if name == "hr":
            trailing = self._children_as_blocks(node)
            return "---" + (f"\n\n{trailing}" if trailing else "")
        if name == "pre":
            return self._convert_pre(node)
        if name in {"ul", "ol"}:
            return self._convert_list(node, ordered=(name == "ol"))
        if name == "li":
            return self._inline(node).strip()
        if name == "blockquote":
            body = self._children_as_blocks(node)
            return "\n".join(f"> {line}" if line else ">" for line in body.splitlines())
        if name == "img":
            return self._convert_image(node)
        if name == "figure":
            return self._children_as_blocks(node)
        if name == "figcaption":
            return self._inline(node).strip()
        if name == "table":
            return self._clean_raw_html(node)
        if name in {"strong", "b"}:
            text = self._inline(node).strip()
            return f"**{text}**" if text else ""
        if name in {"em", "i"}:
            text = self._inline(node).strip()
            return f"*{text}*" if text else ""
        if name == "code":
            if node.find_parent("pre"):
                return node.get_text()
            text = node.get_text().replace("\n", " ").strip()
            if not text:
                return ""
            fence = "`" if "`" not in text else "``"
            return f"{fence}{text}{fence}"
        if name == "a":
            href = node.get("href", "").strip()
            text = self._inline(node).strip()
            if not href:
                return text
            if href.startswith("/"):
                href = urljoin(BASE_URL, href)
            if not text:
                text = href
            return f"[{text}]({href})"
        if name in {"sup", "sub"}:
            return self._clean_raw_html(node)
        if block:
            return self._children_as_blocks(node)
        return self._inline(node)

    def _children_as_blocks(self, tag: Tag) -> str:
        blocks = [self._convert_node(child, block=True).strip() for child in tag.children]
        return "\n\n".join(block for block in blocks if block)

    def _inline(self, tag: Tag) -> str:
        parts = [self._convert_node(child, block=False) for child in tag.children]
        text = "".join(parts)
        text = text.replace("\xa0", " ")
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        return text

    def _convert_pre(self, tag: Tag) -> str:
        code = tag.find("code")
        code_text = code.get_text() if code else tag.get_text()
        language = ""
        classes = list(tag.get("class", [])) + list(code.get("class", []) if code else [])
        for class_name in classes:
            match = re.match(r"(?:language-|lang-)?([A-Za-z0-9_+-]+)$", class_name)
            if match and match.group(1).lower() not in {"nix", "bashshell"}:
                language = match.group(1)
                break
        return f"```{language}\n{code_text.rstrip()}\n```"

    def _convert_list(self, tag: Tag, ordered: bool) -> str:
        lines: list[str] = []
        index = 1
        for child in tag.find_all("li", recursive=False):
            marker = f"{index}. " if ordered else "- "
            body_parts: list[str] = []
            nested_parts: list[str] = []
            for item_child in child.children:
                if isinstance(item_child, Tag) and item_child.name in {"ul", "ol"}:
                    nested = self._convert_list(item_child, ordered=(item_child.name == "ol"))
                    nested_parts.append(indent_lines(nested, "  "))
                else:
                    body_parts.append(self._convert_node(item_child, block=False))
            body = "".join(body_parts).strip()
            body_lines = body.splitlines() or [""]
            lines.append(marker + body_lines[0])
            continuation_prefix = " " * len(marker)
            for line in body_lines[1:]:
                lines.append(continuation_prefix + line)
            lines.extend(nested_parts)
            index += 1
        return "\n".join(lines)

    def _convert_image(self, tag: Tag) -> str:
        src = tag.get("src", "").strip()
        alt = tag.get("alt", "").strip()
        return f"![{alt}]({src})" if src else ""

    def _should_skip(self, tag: Tag) -> bool:
        classes = set(tag.get("class", []))
        return bool(classes & SKIP_CLASSES)

    def _clean_raw_html(self, tag: Tag) -> str:
        for noisy in tag.find_all(["script", "style", "noscript"]):
            noisy.decompose()
        noisy_attrs = {
            "style",
            "class",
            "id",
            "onclick",
            "onerror",
            "border",
            "width",
            "height",
            "cellpadding",
            "cellspacing",
            "align",
            "valign",
            "bgcolor",
        }
        for html_tag in [tag, *tag.find_all(True)]:
            for attr in list(html_tag.attrs):
                if attr.startswith("data-") or attr in noisy_attrs:
                    del html_tag.attrs[attr]
        html = str(tag)
        if tag.name == "table":
            return f'<div class="table-responsive tistory-table">\n{html}\n</div>'
        return html


def indent_lines(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def fetch(session: requests.Session, url: str) -> requests.Response:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response


def discover_posts(session: requests.Session, max_pages: int) -> list[PostSummary]:
    posts: dict[str, PostSummary] = {}
    empty_pages = 0
    for page in range(1, max_pages + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}/?page={page}"
        soup = BeautifulSoup(fetch(session, url).text, "html.parser")
        page_new = 0
        for entry in soup.select("div.list_content"):
            link = entry.select_one("a.link_post[href]")
            if not link:
                continue
            post_url = urljoin(BASE_URL, link["href"])
            post_id = post_url.rstrip("/").rsplit("/", 1)[-1]
            if not post_id.isdigit() or post_id in posts:
                continue
            title_node = entry.select_one(".tit_post")
            category_node = entry.select_one(".detail_info .link_cate")
            date_node = entry.select_one(".detail_info .txt_date")
            posts[post_id] = PostSummary(
                post_id=post_id,
                url=post_url,
                title=clean_text(title_node.get_text(" ", strip=True) if title_node else ""),
                category=clean_text(category_node.get_text(" ", strip=True) if category_node else ""),
                listed_date=clean_text(date_node.get_text(" ", strip=True) if date_node else ""),
            )
            page_new += 1
        empty_pages = empty_pages + 1 if page_new == 0 else 0
        print(f"discovered page {page}: +{page_new} posts", file=sys.stderr)
        if empty_pages >= 2 and posts:
            break
    return sorted(posts.values(), key=lambda post: int(post.post_id), reverse=True)


def parse_post(session: requests.Session, summary: PostSummary) -> tuple[dict, Tag]:
    soup = BeautifulSoup(fetch(session, summary.url).text, "html.parser")
    content = (
        soup.select_one("#article-view .contents_style")
        or soup.select_one("#article-view .tt_article_useless_p_margin")
        or soup.select_one("#article-view")
    )
    if not content:
        raise RuntimeError(f"Could not find article content in {summary.url}")

    for noisy in content.select(".container_postbtn, .another_category, script, style, noscript"):
        noisy.decompose()

    title = meta_content(soup, "og:title") or summary.title
    published = meta_content(soup, "article:published_time") or parse_listed_date(summary.listed_date)
    modified = meta_content(soup, "article:modified_time")
    category = parse_entry_info(soup).get("categoryLabel") or summary.category
    tags = parse_tiara_tags(soup)

    metadata = {
        "title": clean_text(title),
        "published": published,
        "modified": modified,
        "category": clean_text(category),
        "tags": [clean_text(tag) for tag in tags if clean_text(tag)],
    }
    return metadata, content


def meta_content(soup: BeautifulSoup, key: str) -> str:
    node = soup.find("meta", attrs={"property": key}) or soup.find("meta", attrs={"name": key})
    return node.get("content", "").strip() if node else ""


def parse_entry_info(soup: BeautifulSoup) -> dict:
    match = re.search(r"window\.T\.entryInfo\s*=\s*(\{.*?\});", str(soup), flags=re.S)
    if not match:
        return {}
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def parse_tiara_tags(soup: BeautifulSoup) -> list[str]:
    match = re.search(r"window\.tiara\s*=\s*(\{.*?\})</script>", str(soup), flags=re.S)
    if not match:
        return []
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    tags = data.get("entry", {}).get("tags", [])
    return tags if isinstance(tags, list) else []


def parse_listed_date(value: str) -> str:
    value = value.strip()
    for fmt in ("%Y. %m. %d. %H:%M", "%Y. %-m. %-d. %H:%M"):
        try:
            parsed = dt.datetime.strptime(value, fmt)
            return parsed.replace(tzinfo=dt.timezone(dt.timedelta(hours=9))).isoformat()
        except ValueError:
            continue
    return ""


def localize_images(
    session: requests.Session,
    content: Tag,
    post_id: str,
    source_url: str,
    dry_run: bool,
) -> list[dict]:
    image_records: list[dict] = []
    image_dir = IMAGES_DIR / post_id
    if not dry_run:
        image_dir.mkdir(parents=True, exist_ok=True)

    for index, image in enumerate(content.find_all("img"), start=1):
        source = best_image_url(image)
        if not source:
            continue
        local_rel, status = download_image(session, source, image_dir, index, source_url, dry_run)
        if local_rel:
            image["src"] = "/" + local_rel.as_posix()
            for attr in list(image.attrs):
                if attr not in {"src", "alt", "title", "width", "height"}:
                    del image.attrs[attr]
            image_records.append({"source": source, "local": local_rel.as_posix(), "status": status})
        else:
            image_records.append({"source": source, "local": "", "status": status})
    return image_records


def best_image_url(image: Tag) -> str:
    candidates = [
        image.get("data-origin-src"),
        image.get("data-src"),
        image.get("src"),
        image.parent.get("data-url") if isinstance(image.parent, Tag) else "",
        image.parent.get("data-phocus") if isinstance(image.parent, Tag) else "",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        candidate = candidate.strip()
        if "no-image" in candidate:
            continue
        if candidate.startswith("//"):
            return "https:" + candidate
        return candidate
    return ""


def download_image(
    session: requests.Session,
    source: str,
    image_dir: Path,
    index: int,
    referer: str,
    dry_run: bool,
) -> tuple[Path | None, str]:
    if dry_run:
        parsed = urlparse(source)
        suffix = suffix_from_path(parsed.path) or ".img"
        return image_dir / f"image-{index:03d}{suffix}", "dry-run"
    try:
        response = session.get(source, timeout=30, headers={"Referer": referer})
        response.raise_for_status()
    except requests.RequestException as exc:
        return None, f"failed: {exc}"

    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip()
    suffix = mimetypes.guess_extension(content_type) or suffix_from_path(urlparse(source).path) or ".img"
    if suffix == ".jpe":
        suffix = ".jpg"
    target = image_dir / f"image-{index:03d}{suffix}"
    target.write_bytes(response.content)
    return target, "downloaded"


def suffix_from_path(path: str) -> str:
    suffix = Path(posixpath.basename(path)).suffix.lower()
    return suffix if re.fullmatch(r"\.[a-z0-9]{2,5}", suffix) else ""


def write_post(
    summary: PostSummary,
    metadata: dict,
    markdown: str,
    image_records: list[dict],
    dry_run: bool,
) -> Path:
    published = parse_iso_datetime(metadata["published"])
    filename = POSTS_DIR / f"{published:%Y-%m-%d}-tistory-{summary.post_id}.md"
    categories = split_category(metadata["category"])
    front_matter = {
        "layout": "post",
        "title": metadata["title"],
        "date": published.strftime("%Y-%m-%d %H:%M:%S %z"),
        "render_with_liquid": False,
        "categories": categories or ["tistory"],
        "tags": metadata["tags"],
        "tistory_id": int(summary.post_id),
    }
    if metadata.get("modified"):
        front_matter["last_modified_at"] = parse_iso_datetime(metadata["modified"]).strftime(
            "%Y-%m-%d %H:%M:%S %z"
        )
    if has_math(markdown):
        front_matter["use_math"] = True
    if image_records:
        front_matter["imported_images"] = [record["local"] for record in image_records if record["local"]]

    rendered = "---\n"
    rendered += yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False, width=1000)
    rendered += "---\n\n"
    rendered += markdown

    if not dry_run:
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        filename.write_text(rendered, encoding="utf-8")
    return filename


def parse_iso_datetime(value: str) -> dt.datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone(dt.timedelta(hours=9)))
    return parsed


def split_category(category: str) -> list[str]:
    return [part.strip() for part in category.split("/") if part.strip()]


def clean_text(value: str) -> str:
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def has_math(markdown: str) -> bool:
    return bool(re.search(r"\$\$|\\\(|\\\)|\\begin\{|\\frac|\\sum|\\int|\\math", markdown))


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "ko,en;q=0.8"})
    return session


def import_posts(limit: int | None, max_pages: int, dry_run: bool, pause: float) -> int:
    session = build_session()
    converter = HtmlToMarkdown()
    summaries = discover_posts(session, max_pages)
    if limit:
        summaries = summaries[:limit]
    print(f"found {len(summaries)} posts", file=sys.stderr)

    written = 0
    failures: list[str] = []
    for index, summary in enumerate(summaries, start=1):
        try:
            metadata, content = parse_post(session, summary)
            image_records = localize_images(session, content, summary.post_id, summary.url, dry_run)
            markdown = converter.convert(content)
            path = write_post(summary, metadata, markdown, image_records, dry_run)
            print(
                f"[{index}/{len(summaries)}] {summary.post_id}: {path} "
                f"({len(image_records)} images)",
                file=sys.stderr,
            )
            written += 1
        except Exception as exc:  # noqa: BLE001 - keep import going and report all failures.
            failures.append(f"{summary.url}: {exc}")
            print(f"failed {summary.url}: {exc}", file=sys.stderr)
        if pause:
            time.sleep(pause)

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
    return 0 if not failures else 1


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Import only the newest N posts.")
    parser.add_argument("--max-pages", type=int, default=30, help="Maximum index pages to scan.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and convert without writing files.")
    parser.add_argument("--pause", type=float, default=0.15, help="Delay between article imports.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    return import_posts(args.limit, args.max_pages, args.dry_run, args.pause)


if __name__ == "__main__":
    raise SystemExit(main())
