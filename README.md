# Atlas Index

This project is part of a home assignment. The current implementation focuses on collecting knowledge base articles from the OptiSigns Help Center and converting them into clean Markdown files.

## Features

* Pull articles from the OptiSigns Help Center
* Convert HTML content to Markdown
* Preserve headings, links, and code blocks
* Remove navigation and other non-content elements
* Save each article as an individual `.md` file

## Project Structure

```text
.
├── crawler/
│   └── crawl_articles.py
├── docs/
├── main.py
├── requirements.txt
├── .env.sample
└── README.md
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.sample` and configure the required values.

## Run

```bash
python main.py
```

The generated Markdown files will be stored in the `docs/` directory.
