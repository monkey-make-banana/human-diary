"""
Shared types for adapters that pull external evidence.
"""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Protocol


@dataclass
class DocumentRecord:
    id: str
    title: str
    summary: str
    url: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[dt.datetime] = None
    score: Optional[float] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "source": self.source,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "score": self.score,
            "metadata": dict(self.metadata),
        }
        return payload

    def as_langchain_document(self):
        from langchain_core.documents import Document

        metadata = dict(self.metadata)
        metadata["url"] = self.url
        metadata["source"] = self.source
        metadata["published_at"] = (
            self.published_at.isoformat() if self.published_at else None
        )
        metadata["score"] = self.score
        return Document(page_content=self.summary, metadata=metadata)


class SourceAdapter(ABC):
    """
    Contract for wrappers around search / retrieval providers.
    """

    name: str = "source"

    def __init__(self, *, max_results: int = 8) -> None:
        self.max_results = max_results

    @abstractmethod
    async def search(self, query: str) -> List[DocumentRecord]:
        raise NotImplementedError


class SyncAdapter(SourceAdapter):
    """
    Allow sync implementations to plug into the async interface.
    """

    def search_sync(self, query: str) -> List[DocumentRecord]:
        raise NotImplementedError

    async def search(self, query: str) -> List[DocumentRecord]:
        return self.search_sync(query)


class Normalizer(Protocol):
    def __call__(self, records: List[DocumentRecord]) -> List[DocumentRecord]:
        ...


def apply_normalizers(
    records: List[DocumentRecord], normalizers: Optional[List[Normalizer]] = None
) -> List[DocumentRecord]:
    results = records
    for normalize in normalizers or []:
        results = normalize(results)
    return results
