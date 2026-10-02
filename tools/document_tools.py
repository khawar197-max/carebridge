from pathlib import Path


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a plain-text or PDF document.

    This is a basic hackathon document-ingestion tool.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    if path.suffix.lower() == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))

            pages = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n\n".join(pages)

        except ImportError:
            raise RuntimeError(
                "PDF support requires the pypdf package."
            )

    raise ValueError(
        "Unsupported document type. "
        "Please use PDF or TXT."
    )
