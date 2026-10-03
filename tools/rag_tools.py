from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


KNOWLEDGE_DIR = Path("knowledge")

# Lightweight embedding model suitable for semantic retrieval.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def load_knowledge_documents() -> List[str]:
    """
    Load approved trusted knowledge documents.

    Only .txt files inside the knowledge directory
    are treated as trusted knowledge.
    """

    documents = []

    if not KNOWLEDGE_DIR.exists():
        return documents

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):

        try:

            text = file_path.read_text(
                encoding="utf-8"
            )

            if text.strip():

                documents.append(
                    f"Source: {file_path.name}\n\n{text}"
                )

        except Exception:
            continue

    return documents


def split_into_chunks(
    documents: List[str],
    chunk_size: int = 500,
) -> List[str]:
    """
    Split trusted documents into smaller chunks
    for semantic retrieval.
    """

    chunks = []

    for document in documents:

        words = document.split()

        for i in range(
            0,
            len(words),
            chunk_size
        ):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            if chunk.strip():
                chunks.append(chunk)

    return chunks


def build_vector_index(chunks: List[str]):
    """
    Create a FAISS vector index from trusted
    knowledge chunks.
    """

    if not chunks:
        return None

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = embeddings.astype(
        "float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    return index


def retrieve_knowledge(
    query: str,
    top_k: int = 3,
) -> List[str]:
    """
    Perform semantic retrieval over trusted
    CareBridge knowledge.

    Patient-uploaded documents are NEVER added
    to this knowledge index.
    """

    if not query or not query.strip():
        return []

    documents = load_knowledge_documents()

    if not documents:
        return []

    chunks = split_into_chunks(
        documents
    )

    if not chunks:
        return []

    index = build_vector_index(
        chunks
    )

    if index is None:
        return []

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks))
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position < 0:
            continue

        result = (
            f"Semantic relevance score: "
            f"{float(score):.3f}\n\n"
            f"{chunks[index_position]}"
        )

        results.append(result)

    return results
