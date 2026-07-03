import os

import chromadb
from dotenv import load_dotenv
from google import genai

from rag.chunk import build_chunks

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# lưu DB xuống ổ đĩa
chroma = chromadb.PersistentClient(path="vector_db")

collection = chroma.get_or_create_collection(
    name="optisigns_articles"
)

chunks = build_chunks()

print(f"Embedding {len(chunks)} chunks...\n")

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

print("\nDone!")
print(f"Stored {collection.count()} vectors.")