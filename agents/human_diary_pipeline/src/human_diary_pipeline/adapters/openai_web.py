"""
OpenAI Responses API adapter that leverages the built-in web search tool.
"""

from __future__ import annotations

from typing import Any, List, Optional

from openai import AsyncOpenAI

from ..utils.provenance import normalize
from .base import DocumentRecord, SourceAdapter


class OpenAIWebSearchAdapter(SourceAdapter):
    name = "openai_web_search"

    def __init__(
        self,
        api_key: Optional[str],
        *,
        model: str = "o4-mini",
        max_results: int = 5,
    ) -> None:
        super().__init__(max_results=max_results)
        self._client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.model = model

    async def search(self, query: str) -> List[DocumentRecord]:
        if not self._client:
            return []
        response = await self._client.responses.create(
            model=self.model,
            input=f"Return up to {self.max_results} citations with short justifications for: {query}",
            tools=[{"type": "web_search"}],
        )
        records: List[DocumentRecord] = []
        output = response.output or []
        idx = 0
        for item in output:
            if item.type != "message":
                continue
            for content in item.content or []:
                annotations = getattr(content, "annotations", None) or []
                text_value = getattr(content, "text", None)
                snippet = getattr(text_value, "value", None) if text_value else None
                for annotation in annotations[: self.max_results]:
                    url = _get_attr(annotation, "url")
                    title = _get_attr(annotation, "title") or f"OpenAI web result {idx + 1}"
                    idx += 1
                    snippet_value = snippet or _get_attr(annotation, "snippet") or ""
                    score_value = _get_attr(annotation, "score")
                    records.append(
                        DocumentRecord(
                            id=f"openai-web-{idx}",
                            title=title,
                            summary=snippet_value,
                            url=url,
                            source="OpenAI Web Search",
                            metadata={"score": score_value},
                        )
                    )
        return normalize(records)


def _get_attr(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)
