"""
Retriever → cleaner → cluster agents.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Iterable, List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from ..adapters.base import DocumentRecord, SourceAdapter
from ..utils import provenance
from .llm import LLMFactory


def _task_to_query(task: Any) -> str:
    if isinstance(task, dict):
        region = task.get("region", "")
        theme = task.get("theme", "")
        angle = task.get("angle", "")
        return " ".join(part for part in [region, theme, angle] if part)
    return str(task)


class RetrievalAgent:
    def __init__(self, adapters: Iterable[SourceAdapter]) -> None:
        self.adapters = list(adapters)

    async def run(self, tasks: Iterable[Any]) -> Dict[str, Any]:
        records: List[DocumentRecord] = []
        for task in tasks:
            query = _task_to_query(task)
            results = await asyncio.gather(
                *[adapter.search(query) for adapter in self.adapters],
                return_exceptions=True,
            )
            for result in results:
                if isinstance(result, Exception):
                    continue
                records.extend(result)
        return {"raw_documents": records}


class CleanerAgent:
    def __init__(self, max_per_theme: int = 12) -> None:
        self.max_per_theme = max_per_theme

    async def run(self, records: Iterable[DocumentRecord]) -> Dict[str, Any]:
        normalized = provenance.normalize(records)
        normalized.sort(
            key=lambda record: record.published_at.timestamp() if record.published_at else 0.0,
            reverse=True,
        )
        buckets = provenance.cluster_by_domain(normalized)
        curated: List[DocumentRecord] = []
        for _, bucket in buckets.items():
            curated.extend(bucket[: self.max_per_theme])
        return {"clean_documents": curated}


class ClusterAgent:
    def __init__(self, factory: LLMFactory) -> None:
        prompt = PromptTemplate(
            template=(
                "You receive cleaned news records:\n{documents}\n"
                "Group them by theme. Respond with JSON list where each entry has "
                "`label`, `rationale`, and `ids`.\n"
            ),
            input_variables=["documents"],
        )
        self.chain = LLMChain(llm=factory.writer_model(), prompt=prompt, verbose=False)

    async def run(self, records: Iterable[DocumentRecord]) -> Dict[str, Any]:
        doc_lines = [
            f"- ({record.id}) [{record.source}] {record.title} :: {record.summary[:200]}"
            for record in records
        ]
        response = await self.chain.apredict(documents="\n".join(doc_lines))
        try:
            clusters = json.loads(response)
        except json.JSONDecodeError:
            clusters = [{"label": "misc", "rationale": response, "ids": [r.id for r in records]}]
        return {"clusters": clusters, "clean_documents": list(records)}
