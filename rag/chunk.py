from pathlib import Path
import re

DOCS_DIR = Path("docs")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []

    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def load_articles(files):
    articles = []

    for file in files:

        file = Path(file)

        content = file.read_text(encoding="utf-8")

        title = file.stem

        url = ""

        for line in content.splitlines():
            if line.startswith("Article URL:"):
                url = line.replace("Article URL:", "").strip()
                break

        articles.append(
            {
                "title": title,
                "source": file.name,
                "url": url,
                "content": content,
            }
        )

    return articles


def build_chunks(files):
    chunk_list = []

    articles = load_articles(files)

    for article in articles:

        text_chunks = split_text(article["content"])

        for i, chunk in enumerate(text_chunks):

            chunk_list.append(
                {
                    "id": f'{article["title"]}_{i}',
                    "text": chunk,
                    "source": article["source"],
                    "article_url": article["url"],
                }
            )

    return chunk_list


if __name__ == "__main__":

    chunks = build_chunks()

    print(f"Articles : {len(load_articles())}")
    print(f"Chunks   : {len(chunks)}")

    print()

    print(chunks[0])