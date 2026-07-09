# Kakuyomu Scraper

Download all episodes from a [Kakuyomu](https://kakuyomu.jp/) novel as individual text files.

Zero dependencies — Python stdlib only (urllib, json, re).

## Usage

```bash
python kakuyomu_scraper.py
```

Edit `WORK_ID`, `WORK_URL`, and `OUT_DIR` at the top of the script before running.

## Config

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
