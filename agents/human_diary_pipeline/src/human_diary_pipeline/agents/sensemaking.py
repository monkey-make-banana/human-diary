"""
Sense-making agents that convert clusters into impact/uncertainty bullets.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from ..adapters.base import DocumentRecord
from .llm import LLMFactory


class SenseMakingAgent:
    def __init__(self, factory: LLMFactory) -> None:
        prompt = PromptTemplate(
            template=(
                "You are a newsroom sense-maker.\n"
                "Clusters with provenance:\n{clusters}\n\n"
                "For each cluster respond with JSON containing:\n"
                "- `theme`\n- `summary`\n- `impact` (High/Med/Low)\n"
                "- `uncertainty` (High/Med/Low)\n- `why_it_matters`\n"
                "- `citations` (array of source URLs)\n"
            ),
            input_variables=["clusters"],
        )
        self.chain = LLMChain(llm=factory.writer_model(), prompt=prompt, verbose=False)

    async def run(
        self,
        clusters: Iterable[Dict[str, Any]],
        documents: Iterable[DocumentRecord],
    ) -> Dict[str, Any]:
        doc_map = {record.id: record for record in documents}
        cluster_lines: List[str] = []
        for cluster in clusters:
            ids = cluster.get("ids", [])
            refs = [
                f"{doc_map[id_].source}: {doc_map[id_].title}"
                for id_ in ids
                if id_ in doc_map
            ]
            cluster_lines.append(
                f"* {cluster.get('label')}: {cluster.get('rationale')} :: refs={refs}"
            )
        response = await self.chain.apredict(clusters="\n".join(cluster_lines))
        try:
            bullets = json.loads(response)
        except json.JSONDecodeError:
            bullets = [{"theme": "general", "summary": response, "impact": "Med", "uncertainty": "Med"}]
        return {"sensemaking": bullets}
