"""
LangGraph orchestration that mirrors the Humanity's Diary agent stack.
"""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph

from ..adapters.base import DocumentRecord
from ..adapters.registry import adapter_list
from ..agents.llm import LLMFactory
from ..agents.planner import PlannerReviewerLoop
from ..agents.publish import MemoryAgent, PublishAgent
from ..agents.retrieval import CleanerAgent, ClusterAgent, RetrievalAgent
from ..agents.sensemaking import SenseMakingAgent
from ..agents.writing import CriticAgent, DraftAgent, RevisionAgent, SelectorAgent
from ..config import RuntimeConfig


class NewsroomState(TypedDict, total=False):
    planner_directive: str
    tasks: List[Any]
    review: Any
    raw_documents: List[DocumentRecord]
    clean_documents: List[DocumentRecord]
    clusters: List[Dict[str, Any]]
    sensemaking: List[Dict[str, Any]]
    drafts: List[Dict[str, Any]]
    critiques: List[Dict[str, Any]]
    revisions: List[Dict[str, Any]]
    selection: Dict[str, Any]
    publication: Dict[str, Any]
    memory_write: str


def build_default_newsroom(
    config: RuntimeConfig,
    *,
    planner_directive: str | None = None,
):
    factory = LLMFactory(config)
    planner = PlannerReviewerLoop(config, factory)
    retriever = RetrievalAgent(adapter_list(config))
    cleaner = CleanerAgent()
    cluster_agent = ClusterAgent(factory)
    sense_maker = SenseMakingAgent(factory)
    draft_agent = DraftAgent(factory)
    critic = CriticAgent(factory)
    revision = RevisionAgent(factory)
    selector = SelectorAgent(factory)
    publisher = PublishAgent()
    memory = MemoryAgent()

    workflow = StateGraph(NewsroomState)

    async def planner_node(state: NewsroomState) -> NewsroomState:
        directive = (
            state.get("planner_directive")
            or planner_directive
            or config.planner.default_plan
        )
        plan = await planner.run(directive)
        return plan

    async def retrieval_node(state: NewsroomState) -> NewsroomState:
        tasks = state.get("tasks") or []
        return await retriever.run(tasks)

    async def cleaner_node(state: NewsroomState) -> NewsroomState:
        return await cleaner.run(state.get("raw_documents") or [])

    async def cluster_node(state: NewsroomState) -> NewsroomState:
        return await cluster_agent.run(state.get("clean_documents") or [])

    async def sense_node(state: NewsroomState) -> NewsroomState:
        return await sense_maker.run(
            state.get("clusters") or [],
            state.get("clean_documents") or [],
        )

    async def draft_node(state: NewsroomState) -> NewsroomState:
        return await draft_agent.run(
            directive=state.get("planner_directive", ""),
            bullets=state.get("sensemaking") or [],
        )

    async def critic_node(state: NewsroomState) -> NewsroomState:
        return await critic.run(state.get("drafts") or [])

    async def revision_node(state: NewsroomState) -> NewsroomState:
        return await revision.run(state.get("drafts") or [], state.get("critiques") or [])

    async def selector_node(state: NewsroomState) -> NewsroomState:
        return await selector.run(
            directive=state.get("planner_directive", ""),
            revisions=state.get("revisions") or [],
            critiques=state.get("critiques") or [],
        )

    async def publish_node(state: NewsroomState) -> NewsroomState:
        publication = await publisher.run(
            selection=state.get("selection") or {},
            revisions=state.get("revisions") or [],
            sensemaking=state.get("sensemaking") or [],
            review=state.get("review"),
        )
        return {"publication": publication, **publication}

    async def memory_node(state: NewsroomState) -> NewsroomState:
        return await memory.run(state.get("publication") or {}, state.get("review"))

    workflow.add_node("planner", planner_node)
    workflow.add_node("retriever", retrieval_node)
    workflow.add_node("cleaner", cleaner_node)
    workflow.add_node("cluster", cluster_node)
    workflow.add_node("sense", sense_node)
    workflow.add_node("draft", draft_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("revision", revision_node)
    workflow.add_node("selector", selector_node)
    workflow.add_node("publish", publish_node)
    workflow.add_node("memory", memory_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "retriever")
    workflow.add_edge("retriever", "cleaner")
    workflow.add_edge("cleaner", "cluster")
    workflow.add_edge("cluster", "sense")
    workflow.add_edge("sense", "draft")
    workflow.add_edge("draft", "critic")
    workflow.add_edge("critic", "revision")
    workflow.add_edge("revision", "selector")
    workflow.add_edge("selector", "publish")
    workflow.add_edge("publish", "memory")
    workflow.add_edge("memory", END)

    return workflow.compile()
