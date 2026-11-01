import os
import re
from functools import lru_cache
from pathlib import Path
from numbers import Real

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

KB_FILE = Path(__file__).resolve().parent.parent / "knowledge" / "policies.md"

# Matches scoring below this are dropped. 0.0 = keep everything until we calibrate.
MIN_SCORE = float(os.getenv("KB_MIN_SCORE", "0.0"))


def load_chunks() -> list[Document]:
    """Split policies.md into one chunk per '## ' section."""
    text = KB_FILE.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", text)[1:]
    chunks = []
    for section in sections:
            title, _, body = section.partition("\n")
            chunks.append(
                Document(
                     page_content=f"{title.strip()}\n{body.strip()}",
                     metadata={"section_title": title.strip()},
                )
            )
    return chunks

@lru_cache(maxsize=1)
def get_store() -> InMemoryVectorStore:
    """Build the searchable index once, the first time it is needed."""
    embeddings = OllamaEmbeddings(model=os.getenv("EMBED_MODEL", "nomic-embed-text"))
    store = InMemoryVectorStore(embeddings)
    store.add_documents(load_chunks())
    return store

def search_policies(query: str, k: int = 2) -> list[Document]:
    raw = get_store().similarity_search_with_score(query, k=k)

    results = []
    for item in raw:
        # Find the Document and the score by TYPE, not by position
        doc = next((x for x in item if isinstance(x, Document)), None)
        score = next(
            (x for x in item if isinstance(x, Real) and not isinstance(x, bool)),
            0.0,
        )
        if doc is None:
            print(f"  [kb] unexpected result shape: {[type(x).__name__ for x in item]}")
            continue
        results.append((doc, float(score)))

    if os.getenv("KB_DEBUG") == "1":
        for doc, score in results:
            title = doc.page_content.split("\n")[0]
            print(f"  [kb] {score:.3f}  {title}")

    return [doc for doc, score in results if score >= MIN_SCORE]