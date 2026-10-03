from pathlib import Path
from typing import List


KNOWLEDGE_DIR = Path("knowledge")


def load_knowledge_documents() -> List[str]:
    """
    Load approved text documents from the CareBridge
    trusted knowledge directory.

    Only .txt files are included.
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


def retrieve_knowledge(
    query: str,
    top_k: int = 3
) -> List[str]:
    """
    Simple deterministic keyword-based retrieval.

    This is the first RAG layer for CareBridge.
    It retrieves information only from approved
    knowledge documents.

    It does not use patient documents as knowledge sources.
    """

    if not query or not query.strip():
        return []

    documents = load_knowledge_documents()

    if not documents:
        return []

    query_words = {
        word.lower().strip(".,:;!?()[]{}")
        for word in query.split()
        if len(word.strip()) > 2
    }

    scored_documents = []

    for document in documents:

        document_lower = document.lower()

        score = sum(
            1
            for word in query_words
            if word in document_lower
        )

        if score > 0:

            scored_documents.append(
                (score, document)
            )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        document
        for _, document in scored_documents[:top_k]
    ]
