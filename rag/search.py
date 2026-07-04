import os

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

db = chromadb.PersistentClient(path="vector_db")

collection = db.get_collection("optisigns_articles")


def search(query: str, top_k: int = 5):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
    )

    embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":

    question = "How do I add a YouTube video?"

    results = search(question)

    for i in range(len(results["documents"][0])):

        print("=" * 80)

        print(results["metadatas"][0][i]["article_url"])

        print()

        print(results["documents"][0][i][:400])

        print()