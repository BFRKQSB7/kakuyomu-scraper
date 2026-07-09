# Kakuyomu Scraper（カクヨム下载器）

> 下载 [Kakuyomu](https://kakuyomu.jp/) 小说的全部章节为独立文本文件。零依赖。

[**English**](./docs/en/README.md) | **中文简体** | [**日本語**](./docs/ja/README.md)

## 功能

- **零依赖** — 仅使用 Python 标准库（`urllib`、`json`、`re`）
- **自动发现** — 从作品页面的 `__NEXT_DATA__` JSON 中解析全部章节列表
- **干净输出** — 去除 HTML 标签、注音标记，按段落格式化纯文本

## 快速开始

```bash
python kakuyomu_scraper.py
```

运行前修改脚本顶部的以下变量：

| 变量       | 说明                         |
|------------|------------------------------|
| `WORK_ID`  | Kakuyomu 作品 ID（从 URL 获取） |
| `WORK_URL` | 作品页完整 URL                |
| `OUT_DIR`  | `.txt` 文件输出目录           |
| `DELAY`    | 请求间隔秒数（默认 0.5）      |

## 输出格式

每章保存为 `001.txt`、`002.txt` …，包含元数据头部：

```
# URL: https://kakuyomu.jp/works/.../episodes/...
# Chapter: <章节名>
# Title: <标题>

<正文>
```

## 文件结构

```
kakuyomu-scraper/
├── kakuyomu_scraper.py     # 主脚本
├── docs/
│   ├── en/README.md        # English
│   └── ja/README.md        # 日本語
├── README.md
└── .gitignore
```

## 许可证

MIT
