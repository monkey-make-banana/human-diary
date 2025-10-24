"""
NewsAPI adapter for structured global coverage.
"""

from __future__ import annotations

import datetime as dt
from typing import List, Optional

import httpx

from ..utils.provenance import normalize
from .base import DocumentRecord, SyncAdapter


class NewsApiAdapter(SyncAdapter):
    name = "newsapi"
    endpoint = "https://newsapi.org/v2/everything"

    def __init__(
        self,
        api_key: Optional[str],
        *,
        max_results: int = 10,
        timeout: float = 10.0,
        language: str = "en",
    ) -> None:
        super().__init__(max_results=max_results)
        self.api_key = api_key
        self.timeout = timeout
        self.language = language

    def _parse_time(self, raw: Optional[str]) -> Optional[dt.datetime]:
        if not raw:
            return None
        try:
            return dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None

    def search_sync(self, query: str) -> List[DocumentRecord]:
        if not self.api_key:
            return []
        params = {
            "q": query,
            "language": self.language,
            "sortBy": "publishedAt",
            "pageSize": self.max_results,
        }
        headers = {"X-Api-Key": self.api_key}
        response = httpx.get(self.endpoint, params=params, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        articles = payload.get("articles", [])
        records: List[DocumentRecord] = []
        for idx, article in enumerate(articles[: self.max_results]):
            source_name = (article.get("source") or {}).get("name")
            records.append(
                DocumentRecord(
                    id=article.get("url") or f"newsapi-{idx}",
                    title=article.get("title") or "Untitled article",
                    summary=article.get("description") or article.get("content") or "",
                    url=article.get("url"),
                    source=source_name,
                    published_at=self._parse_time(article.get("publishedAt")),
                    metadata={
                        "author": article.get("author"),
                        "image": article.get("urlToImage"),
                    },
                )
            )
        return normalize(records)
