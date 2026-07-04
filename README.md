# Atlas Index

Atlas Index collects OptiSigns Help Center articles, converts them into clean Markdown files, and prepares them for semantic search with a small RAG assistant.

## What the project does

* Crawls knowledge base articles from the OptiSigns Help Center API
* Cleans HTML by removing navigation, footer, sidebar, and other non-content elements
* Converts article content into Markdown
* Saves each article as its own `.md` file
* Splits the generated docs into chunks for embedding and search
* Uses ChromaDB and Gemini embeddings to answer questions from the local article set

## Project Structure

```text
.
├── app/                  # reserved for future application modules or shared code
├── assistant/            # Gemini-powered question answering on top of indexed docs
│   └── chat.py           # interactive chat loop that queries the local article index
├── crawler/              # article collection and markdown export logic
│   └── crawl_articles.py # fetches help-center articles, cleans HTML, and writes .md files
├── docs/                 # generated markdown articles used by the RAG pipeline
├── rag/                  # chunking, embedding, and semantic search helpers
│   ├── chunk.py          # loads markdown docs and splits them into searchable chunks
│   ├── ingest.py         # embeds chunks and stores them in ChromaDB
│   ├── list_models.py    # prints available Gemini models
│   ├── search.py         # embeds a query and retrieves matching chunks
│   └── test_embedding.py # simple embedding smoke test for Gemini API access
├── vector_db/            # persistent ChromaDB storage for embeddings
├── logs/                 # runtime logs, if you choose to capture them
├── .env.sample           # example environment variables for local setup
├── .gitignore            # ignores generated files, local env files, caches, and logs
├── Dockerfile            # container image definition for the project
├── requirements.txt      # Python dependencies needed for crawling and RAG
├── README.md             # project overview, file meanings, and usage instructions
└── main.py               # entry point that starts the crawl process
```

## File meanings

* `main.py` is the entry point. It imports the crawler flow and runs `crawl()` when executed.
* `crawler/crawl_articles.py` reads `API_URL`, fetches paginated article data, cleans HTML, converts it to Markdown, and writes each article into `docs/`.
* `docs/` stores the generated Markdown articles that later feed the chunking and embedding pipeline.
* `rag/chunk.py` reads every Markdown file in `docs/`, splits the text into chunks, and attaches article metadata.
* `rag/ingest.py` sends each chunk to Gemini embeddings and saves the vectors into the local ChromaDB database in `vector_db/`.
* `rag/search.py` embeds a user query and searches the Chroma collection for relevant chunks.
* `assistant/chat.py` wraps search in a simple chat loop and asks Gemini to answer using only the retrieved context.
* `rag/list_models.py` prints available Gemini model names for quick environment checks.
* `rag/test_embedding.py` is a lightweight smoke test that verifies Gemini embedding access and prints the vector length.
* `vector_db/` stores the persistent ChromaDB database created during ingestion.
* `app/` is currently reserved for future application-level code.
* `assistant/` contains the local support assistant for the indexed docs.
* `crawler/` contains the code that collects and exports article content.
* `logs/` is reserved for runtime logs if you add logging later.
* `.env.sample` documents the environment variables the scripts expect.
* `.gitignore` keeps generated artifacts, local environment files, caches, and logs out of git.
* `requirements.txt` lists the Python packages needed for crawling, chunking, embedding, and chat.
* `Dockerfile` defines how to build the app inside a container.
* `README.md` explains the project layout, setup, flow, and test case.

## Chunking Strategy

The crawler converts each OptiSigns Help Center article into a Markdown file. During indexing, each document is split into fixed-size text chunks before generating embeddings.

- **Chunk size:** 800 characters
- **Chunk overlap:** 150 characters

This approach was chosen to balance retrieval quality and efficiency:

- Each chunk is large enough to preserve the context of a section or several related steps.
- A 150-character overlap helps maintain continuity between adjacent chunks and reduces the chance of losing important information at chunk boundaries.
- Smaller chunks generally improve retrieval precision, while the overlap ensures that content spanning two chunks can still be retrieved correctly.

This strategy is simple, lightweight, and works well for the structured documentation used in the OptiSigns Help Center.

## Flow Test Case

### Test Case: Crawl Article To Search Result Flow

**Goal:** verify the full local pipeline from crawling articles to searching the indexed content.

**Preconditions:**

* `.env` exists and contains valid values for `OPTISIGNS_BASE_URL`, `API_URL`, `OUTPUT_DIR`, `MAX_ARTICLES`, and `GEMINI_API_KEY`
* `docs/` is writable
* `vector_db/` is writable

**Steps:**

1. Run the crawler with `python main.py`.
2. Confirm that one or more Markdown files are created in `docs/`.
3. Open a generated Markdown file and verify it contains a title, optional `Article URL:`, a separator line, and article content.
4. Run `python -m rag.ingest` to chunk the docs and create embeddings.
5. Run `python -m rag.search` and search for a question related to one of the crawled articles.
6. Optionally run `python -m assistant.chat` and ask a question from the same article set.

**Expected result:**

* The crawler saves Markdown articles into `docs/`
* `rag.ingest` stores vectors in the local ChromaDB collection `optisigns_articles`
* `rag.search` returns relevant article chunks and their source URLs
* `assistant.chat` answers using only the retrieved context and prints up to three `Article URL:` lines

**Suggested sample question:**

```text
How do I add a YouTube video in OptiSigns?
```

## Environment Variables

Create a `.env` file from `.env.sample` and set the values for your environment.

Typical variables used by the code are:

* `OPTISIGNS_BASE_URL` - base website URL for the source system
* `API_URL` - article API endpoint used by the crawler
* `OUTPUT_DIR` - directory where markdown files are written
* `MAX_ARTICLES` - maximum number of articles to crawl
* `GEMINI_API_KEY` - API key used by the embedding and chat scripts

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the crawler

```bash
python main.py
```

This generates markdown articles in `docs/`.

## Build embeddings and search

After the docs are generated, run the ingestion script to populate ChromaDB:

```bash
python -m rag.ingest
```

Then you can search the indexed content or start the assistant:

```bash
python -m rag.search
python -m assistant.chat
```

## Notes

The repository currently uses `docs/` for generated article files and `vector_db/` for the persisted embedding store. If you also create `embeddings/` locally for experimental exports, treat it as generated output. `logs/` is also safe to use for runtime output.
