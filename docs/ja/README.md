# Kakuyomu Scraper（カクヨム スクレイパー）

> [カクヨム](https://kakuyomu.jp/)の小説を全話まとめてテキストファイルに保存。依存ライブラリなし。

[**English**](../../README.md) | [**中文简体**](../cn/README.md) | **日本語**

## 機能

- **依存ゼロ** — Python 標準ライブラリのみ（`urllib`、`json`、`re`）
- **自動検出** — 作品ページの `__NEXT_DATA__` JSON から全エピソードを抽出
- **クリーン出力** — HTML タグ・ルビを除去、段落区切りでプレーンテキスト化

## クイックスタート

```bash
python kakuyomu_scraper.py
```

実行前にスクリプト冒頭の変数を編集：

| 変数       | 説明                              |
|------------|-----------------------------------|
| `WORK_ID`  | カクヨム作品 ID（URL から取得）     |
| `WORK_URL` | 作品ページの URL                   |
| `OUT_DIR`  | `.txt` ファイルの出力先            |
| `DELAY`    | リクエスト間隔（秒、デフォルト 0.5）|

## 出力形式

各エピソードを `001.txt`、`002.txt` … として保存。メタデータヘッダ付き：

```
# URL: https://kakuyomu.jp/works/.../episodes/...
# Chapter: <チャプター名>
# Title: <タイトル>

<本文>
```

## ファイル構成

```
kakuyomu-scraper/
├── kakuyomu_scraper.py     # メインスクリプト
├── docs/
│   ├── cn/README.md        # 中文简体
│   └── ja/README.md        # 日本語
├── README.md
└── .gitignore
```

## ライセンス

MIT
