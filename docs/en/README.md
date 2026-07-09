# Kakuyomu Scraper

> Download all episodes from a [Kakuyomu](https://kakuyomu.jp/) novel as individual text files. Zero dependencies.

**English** | [**中文简体**](../../README.md) | [**日本語**](../ja/README.md)

## Features

- **Zero dependencies** — Python stdlib only (`urllib`, `json`, `re`)
- **Auto-discovery** — parses `__NEXT_DATA__` JSON from the work page to list all episodes
- **Clean output** — strips HTML tags, ruby annotations, formats paragraphs as plain text

## Quick Start

```bash
python kakuyomu_scraper.py
```

Edit these variables at the top of the script before running:

| Variable   | Description                          |
|------------|--------------------------------------|
| `WORK_ID`  | Kakuyomu work ID (from URL)          |
| `WORK_URL` | Full work page URL                   |
| `OUT_DIR`  | Output directory for `.txt` files    |
| `DELAY`    | Seconds between requests (default 0.5) |

## Output

Each episode saved as `001.txt`, `002.txt`, ... with metadata header:

```
# URL: https://kakuyomu.jp/works/.../episodes/...
# Chapter: <chapter name>
# Title: <episode title>

<body text>
```

## File Structure

```
kakuyomu-scraper/
├── kakuyomu_scraper.py     # Main script
├── docs/
│   ├── en/README.md        # English
│   └── ja/README.md        # 日本語
├── README.md
└── .gitignore
```

## License

MIT
