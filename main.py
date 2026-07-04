from crawler.crawl_articles import crawl
from rag.ingest import ingest


def main():
    result = crawl()

    changed_files = result["changed_files"]

    if changed_files:
        print("\nUploading delta to vector database...\n")
        ingest(changed_files)
    else:
        print("\nNo new or updated articles found.")


if __name__ == "__main__":
    main()