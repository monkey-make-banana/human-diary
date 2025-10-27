"""
Semantic Scholar search adapter.
"""

from __future__ import annotations

import datetime as dt
from typing import List, Optional

import httpx

from ..utils.provenance import normalize
from .base import DocumentRecord, SyncAdapter


class SemanticScholarAdapter(SyncAdapter):
    name = "semantic_scholar"
    search_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(
        self,
        api_key: Optional[str],
        *,
        max_results: int = 10,
        timeout: float = 10.0,
    ) -> None:
        super().__init__(max_results=max_results)
        self.api_key = api_key
        self.timeout = timeout

    def _parse_date(self, value: Optional[str]) -> Optional[dt.datetime]:
        if not value:
            return None
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    def search_sync(self, query: str) -> List[DocumentRecord]:
        params = {
            "query": query,
            "limit": self.max_results,
            "fields": "title,url,abstract,publicationDate,tldr,externalIds,authors",
        }
        headers = {"accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        response = httpx.get(
            self.search_url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        records: List[DocumentRecord] = []
        for paper in payload.get("data", []):
            record = DocumentRecord(
                id=str(paper.get("paperId")),
                title=paper.get("title") or "Untitled",
                summary=paper.get("tldr", {}).get("text")
                or paper.get("abstract")
                or "No summary",
                url=paper.get("url") or paper.get("openAccessPdf", {}).get("url"),
                source="Semantic Scholar",
                published_at=self._parse_date(paper.get("publicationDate")),
                score=paper.get("score"),
                metadata={
                    "authors": [author.get("name") for author in paper.get("authors", [])],
                    "external_ids": paper.get("externalIds", {}),
                },
            )
            records.append(record)
        return normalize(records)
