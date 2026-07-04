import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai

from rag.chunk import build_chunks

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Persistent local vector database
chroma = chromadb.PersistentClient(path="vector_db")

collection = chroma.get_or_create_collection(
    name="optisigns_articles"
)


def ingest(files):
    """
    Embed only new/updated markdown files.
    """

    if not files:
        print("No new or updated files to embed.")
        return

    # Remove old vectors of updated files
    for file in files:
        collection.delete(
            where={
                "source": Path(file).name
            }
        )

    chunks = build_chunks(files)

    print(f"\nEmbedding {len(chunks)} chunks...\n")

    embedded = 0

    for i, chunk in enumerate(chunks, start=1):

        print(f"[{i}/{len(chunks)}] {chunk['id']}")

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk["text"],
        )

        embedding = response.embeddings[0].values

        collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[
                {
                    "source": chunk["source"],
                    "article_url": chunk["article_url"],
                }
            ],
        )

        embedded += 1

    print("\n===== Embedding Summary =====")
    print(f"Files processed : {len(files)}")
    print(f"Chunks embedded : {embedded}")
    print(f"Total vectors   : {collection.count()}")
    print("=============================")


if __name__ == "__main__":
    docs = list(Path("docs").glob("*.md"))
    ingest(docs)