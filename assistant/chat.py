import os

from dotenv import load_dotenv
from google import genai

from rag.search import search

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are OptiBot, the customer-support bot for OptiSigns.com.

Tone: helpful, factual, concise.

Only answer using the uploaded docs.

Max 5 bullet points; else link to the doc.

Cite up to 3 "Article URL:" lines per reply.
"""


def ask(question: str):

    results = search(question, top_k=5)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""

    urls = []

    for doc, meta in zip(docs, metas):

        context += doc
        context += "\n\n----------------------\n\n"

        if meta["article_url"] not in urls:
            urls.append(meta["article_url"])

    prompt = f"""
Context:

{context}

Question:
{question}

Answer ONLY using the context above.
If the answer is not contained in the context, say you don't know.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
    )

    print("\n")
    print(response.text)

    print("\n")

    for url in urls[:3]:
        print(f"Article URL: {url}")


if __name__ == "__main__":

    while True:

        question = input("\nQuestion: ")

        if question.lower() in ["exit", "quit"]:
            break

        ask(question)