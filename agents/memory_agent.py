from typing import List

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    memory: str
    source: str
    relevance: str


class MemoryResult(BaseModel):
    memories: List[MemoryItem] = Field(
        default_factory=list
    )
    requires_human_review: bool = False


class MemoryAgent:
    """
    Retrieves previously approved CareBridge interaction
    information for continuity.

    Memory is supporting context only.

    It must never:
    - diagnose
    - prescribe
    - override safety decisions
    - override trusted knowledge
    - make independent medical decisions
    """

    name = "Memory Agent"

    def __init__(self, llm):
        self.llm = llm

    def retrieve(
        self,
        query: str,
        memories: List[str]
    ) -> MemoryResult:

        if not memories:
            return MemoryResult(
                memories=[]
            )

        # For the first version, memory retrieval is
        # intentionally simple and deterministic.
        query_words = set(
            query.lower().split()
        )

        results = []

        for memory in memories:

            memory_words = set(
                memory.lower().split()
            )

            overlap = (
                query_words.intersection(
                    memory_words
                )
            )

            if overlap:

                results.append(
                    MemoryItem(
                        memory=memory,
                        source="CareBridge Memory",
                        relevance=(
                            "Relevant terms matched "
                            "the current request."
                        ),
                    )
                )

        return MemoryResult(
            memories=results,
            requires_human_review=False,
        )
