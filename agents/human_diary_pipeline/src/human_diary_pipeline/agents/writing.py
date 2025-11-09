"""
Draft → critic → revision → selector agents.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .llm import LLMFactory


class DraftAgent:
    def __init__(self, factory: LLMFactory, variants: int = 2) -> None:
        self.variants = variants
        prompt = PromptTemplate(
            template=(
                "You are the lead writer for Humanity's Diary.\n"
                "Planner directive:\n{directive}\nSense-making bullets:\n{bullets}\n\n"
                f"Produce {variants} narrative variants as JSON list where each entry "
                "has `id`, `lede`, `body`, and `provenance_notes`."
            ),
            input_variables=["directive", "bullets"],
        )
        self.chain = LLMChain(llm=factory.writer_model(), prompt=prompt, verbose=False)

    async def run(self, directive: str, bullets: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        response = await self.chain.apredict(
            directive=directive,
            bullets=json.dumps(list(bullets), indent=2),
        )
        try:
            variants = json.loads(response)
        except json.JSONDecodeError:
            variants = [{"id": "draft-1", "lede": "", "body": response, "provenance_notes": ""}]
        return {"drafts": variants}


class CriticAgent:
    def __init__(self, factory: LLMFactory) -> None:
        prompt = PromptTemplate(
            template=(
                "Review the following draft variant for factuality, balance, and narrative clarity.\n"
                "Draft JSON:\n{draft}\n\n"
                "Respond with JSON containing `scores` (0-1 for factuality/balance/story) "
                "and `revision_notes`."
            ),
            input_variables=["draft"],
        )
        self.chain = LLMChain(llm=factory.critic_model(), prompt=prompt, verbose=False)

    async def run(self, drafts: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        critiques: List[Dict[str, Any]] = []
        for draft in drafts:
            response = await self.chain.apredict(draft=json.dumps(draft, indent=2))
            try:
                critique = json.loads(response)
            except json.JSONDecodeError:
                critique = {"scores": {"factuality": 0.6, "balance": 0.6, "story": 0.6}, "revision_notes": response}
            critique["id"] = draft.get("id")
            critiques.append(critique)
        return {"critiques": critiques}


class RevisionAgent:
    def __init__(self, factory: LLMFactory) -> None:
        prompt = PromptTemplate(
            template=(
                "You are revising a newsroom draft.\nDraft:\n{draft}\nCritique:\n{critique}\n"
                "Return improved draft JSON with same keys."
            ),
            input_variables=["draft", "critique"],
        )
        self.chain = LLMChain(llm=factory.writer_model(), prompt=prompt, verbose=False)

    async def run(
        self,
        drafts: Iterable[Dict[str, Any]],
        critiques: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        critique_map = {critique.get("id"): critique for critique in critiques}
        revised: List[Dict[str, Any]] = []
        for draft in drafts:
            critique = critique_map.get(draft.get("id"))
            response = await self.chain.apredict(
                draft=json.dumps(draft, indent=2),
                critique=json.dumps(critique or {}, indent=2),
            )
            try:
                revision = json.loads(response)
            except json.JSONDecodeError:
                revision = {**draft, "body": response}
            revision["id"] = draft.get("id")
            revised.append(revision)
        return {"revisions": revised}


class SelectorAgent:
    def __init__(self, factory: LLMFactory) -> None:
        prompt = PromptTemplate(
            template=(
                "Select the best version for publication.\n"
                "Directive: {directive}\n"
                "Revisions: {revisions}\n"
                "Critiques: {critiques}\n"
                "Respond with JSON `winner_id` and `justification`."
            ),
            input_variables=["directive", "revisions", "critiques"],
        )
        self.chain = LLMChain(llm=factory.critic_model(), prompt=prompt, verbose=False)

    async def run(
        self,
        directive: str,
        revisions: Iterable[Dict[str, Any]],
        critiques: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        response = await self.chain.apredict(
            directive=directive,
            revisions=json.dumps(list(revisions), indent=2),
            critiques=json.dumps(list(critiques), indent=2),
        )
        try:
            decision = json.loads(response)
        except json.JSONDecodeError:
            decision = {"winner_id": "draft-1", "justification": response}
        return {"selection": decision}
