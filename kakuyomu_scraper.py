"""
Kakuyomu novel downloader — all episodes as individual text files.
Zero dependencies (Python stdlib only: urllib, json, re).

Usage: python kakuyomu_scraper.py
"""
import urllib.request
import json
import time
import os
import re

WORK_ID = "16818093077820666277"
WORK_URL = f"https://kakuyomu.jp/works/{WORK_ID}"
OUT_DIR = r"C:\Users\NYRO\Desktop\1"
DELAY = 0.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}


def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            print(f"  [retry {attempt+1}/{retries}] {e}")
            time.sleep(2 ** attempt)
    return None


def extract_episodes_from_json(html):
    """Parse __NEXT_DATA__ JSON to get all (episode_id, title, chapter) tuples."""
    m = re.search(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not m:
        raise RuntimeError("Cannot find __NEXT_DATA__ script tag")

    data = json.loads(m.group(1))
    apollo = data.get("props", {}).get("pageProps", {}).get("__APOLLO_STATE__", {})
    if not apollo:
        raise RuntimeError("Cannot find Apollo state")

    # Gather all TableOfContentsChapter entries
    episodes = []
    for key, toc_ch in apollo.items():
        if not key.startswith("TableOfContentsChapter:"):
            continue

        # Resolve chapter title (chapter can be explicitly null in JSON)
        ch_ref = (toc_ch.get("chapter") or {}).get("__ref", "")
        ch_data = apollo.get(ch_ref, {})
        ch_title = ch_data.get("title", "")

        # Walk episodeUnions
        for ep_ref in (toc_ch.get("episodeUnions") or []):
            ep_key = ep_ref.get("__ref", "")
            ep_data = apollo.get(ep_key, {})
            episodes.append((
                ep_data.get("id", ""),
                ep_data.get("title", ""),
                ch_title,
            ))

    return episodes


def parse_episode_body(html):
    """Extract title, chapter headers, and body from episode page (regex, no BS)."""

    def tag_text(tag_class):
        """Get inner text of first <p class="TAG"> element."""
        m = re.search(
            r'<p\s+class="' + re.escape(tag_class) + r'[^"]*"[^>]*>(.*?)</p>',
            html, re.DOTALL
        )
        if not m:
            return ""
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()

    title = tag_text("widget-episodeTitle")
    ch1 = tag_text("chapterTitle level1")
    ch2 = tag_text("chapterTitle level2")

    # Body: find widget-episodeBody div
    body_m = re.search(
        r'<div\s+class="widget-episodeBody[^"]*"[^>]*>(.*?)</div>\s*(?:</article>|<div\s+class="widget-episode)',
        html, re.DOTALL
    )
    if not body_m:
        # Fallback: grab everything up to next closing div at same indent level
        body_m = re.search(
            r'<div\s+class="widget-episodeBody[^"]*"[^>]*>(.*?)</div>',
            html, re.DOTALL
        )
    if not body_m:
        return title, ch1, ch2, ""

    raw = body_m.group(1)

    # Clean body
    text = raw

    # Remove ruby annotations (keep base text)
    text = re.sub(r'<ruby>(.*?)<rt>.*?</rt></ruby>', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'<ruby>([^<]*)<rp>.*?</rp><rt>.*?</rt></ruby>', r'\1', text)

    # Blank paragraphs → empty line
    text = re.sub(r'<p\s+class="blank[^"]*"[^>]*>.*?</p>', '\n', text, flags=re.DOTALL)

    # Line breaks
    text = re.sub(r'<br\s*/?>', '\n', text)

    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#x27;', "'")

    # Numeric entities
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    text = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), text)

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return title, ch1, ch2, text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Fetching TOC: {WORK_URL}")
    html = fetch_url(WORK_URL)
    if not html:
        print("FATAL: Cannot fetch work page")
        return

    print("Parsing episode list from __NEXT_DATA__...")
    episodes = extract_episodes_from_json(html)
    total = len(episodes)
    print(f"Found {total} episodes\n")

    success = fail = 0

    for idx, (ep_id, ep_title, chapter) in enumerate(episodes, 1):
        ep_url = f"https://kakuyomu.jp/works/{WORK_ID}/episodes/{ep_id}"
        fname = f"{idx:03d}.txt"
        fpath = os.path.join(OUT_DIR, fname)
        header = f"# URL: {ep_url}\n# Chapter: {chapter}\n# Title: {ep_title}\n\n"

        short = ep_title[:50]
        print(f"[{idx}/{total}] {short}...", end=" ", flush=True)

        ep_html = fetch_url(ep_url)
        if not ep_html:
            print("FAILED")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(header + "[DOWNLOAD FAILED]")
            fail += 1
            time.sleep(DELAY)
            continue

        title, ch1, ch2, body = parse_episode_body(ep_html)

        full_text = header + body
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"OK ({len(body)} chars)")
        success += 1
        time.sleep(DELAY)

    print(f"\nDone! {success} OK, {fail} failed → {OUT_DIR}")


if __name__ == "__main__":
    main()
