"""
SerpAPI News adapter.
"""

from __future__ import annotations

import datetime as dt
from typing import List, Optional

import httpx

from ..utils.provenance import normalize
from .base import DocumentRecord, SyncAdapter


class SerpApiNewsAdapter(SyncAdapter):
    name = "serpapi_news"
    endpoint = "https://serpapi.com/search.json"

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
            "engine": "google_news",
            "q": query,
            "api_key": self.api_key,
            "num": self.max_results,
        }
        response = httpx.get(self.endpoint, params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        stories = payload.get("news_results", [])
        records: List[DocumentRecord] = []
        for story in stories[: self.max_results]:
            records.append(
                DocumentRecord(
                    id=story.get("id") or story.get("link"),
                    title=story.get("title") or "Untitled story",
                    summary=story.get("snippet") or "",
                    url=story.get("link"),
                    source=story.get("source"),
                    published_at=self._parse_time(story.get("date")),
                    metadata={
                        "thumbnail": story.get("thumbnail"),
                        "topic": story.get("topic"),
                        "source_url": story.get("source_url"),
                    },
                )
            )
        return normalize(records)
