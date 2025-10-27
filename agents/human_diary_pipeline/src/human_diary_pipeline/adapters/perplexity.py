"""
Perplexity Sonar adapter powered by the public chat completions endpoint.
"""

from __future__ import annotations

import datetime as dt
import json
from typing import List, Optional

import httpx

from ..utils.provenance import normalize
from .base import DocumentRecord, SyncAdapter


class PerplexitySonarAdapter(SyncAdapter):
    name = "perplexity_sonar"
    endpoint = "https://api.perplexity.ai/chat/completions"

    def __init__(
        self,
        api_key: Optional[str],
        *,
        model: str = "sonar-reasoning",
        max_results: int = 5,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(max_results=max_results)
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def search_sync(self, query: str) -> List[DocumentRecord]:
        if not self.api_key:
            return []
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}",
        }
        messages = [
            {"role": "system", "content": "You are a research assistant returning JSON bulletins."},
            {
                "role": "user",
                "content": f"Return {self.max_results} concise findings with links about: {query}",
            },
        ]
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "return_citations": True,
        }
        response = httpx.post(
            self.endpoint,
            headers=headers,
            content=json.dumps(payload),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content")
        citations = message.get("citations") or []
        records: List[DocumentRecord] = []
        for idx, citation in enumerate(citations[: self.max_results]):
            link = citation.get("url")
            title = citation.get("title") or f"Perplexity finding {idx + 1}"
            snippet = citation.get("snippet") or content
            timestamp = citation.get("published_date")
            published_at = (
                dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                if timestamp
                else None
            )
            records.append(
                DocumentRecord(
                    id=f"perplexity-{idx}",
                    title=title,
                    summary=snippet or "No summary provided",
                    url=link,
                    source="Perplexity Sonar",
                    published_at=published_at,
                    metadata={"raw": citation},
                )
            )
        if not records and content:
            records.append(
                DocumentRecord(
                    id="perplexity-summary",
                    title="Perplexity Sonar Summary",
                    summary=content,
                    source="Perplexity Sonar",
                    metadata={"citations": citations},
                )
            )
        return normalize(records)
