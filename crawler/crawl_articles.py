import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from slugify import slugify

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OPTISIGNS_BASE_URL")
API_URL = os.getenv("API_URL")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES"))

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove navigation / ads / related articles if they exist
    remove_selectors = [
        "nav",
        "header",
        "footer",
        "aside",
        ".breadcrumbs",
        ".related-articles",
        ".article-votes",
        ".article-footer",
        ".article-sidebar",
        ".share",
        ".advertisement",
        ".ads",
    ]

    for selector in remove_selectors:
        for tag in soup.select(selector):
            tag.decompose()

    return str(soup)


def html_to_markdown(html):
    return md(
        html,
        heading_style="ATX",
        bullets="-",
        strip=["style", "script"],
    )


def save_article(article):
    title = article["title"]
    body = article["body"]
    article_url = article.get("html_url", "")

    html = clean_html(body)
    markdown = html_to_markdown(html)

    filename = slugify(title) + ".md"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")

        if article_url:
            f.write(f"Article URL: {article_url}\n\n")

        f.write("---\n\n")
        f.write(markdown)

    print("Saved:", filename)


def crawl():
    url = API_URL
    total = 0

    while url:

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        for article in data["articles"]:
            save_article(article)
            total += 1

            if total >= MAX_ARTICLES:
                print("Done.")
                return

        url = data["next_page"]