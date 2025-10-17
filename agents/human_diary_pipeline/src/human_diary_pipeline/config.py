"""
Centralized configuration management for the newsroom pipeline.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class ApiConfig(BaseModel):
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    serpapi_api_key: Optional[str] = Field(default=None, alias="SERPAPI_API_KEY")
    newsapi_key: Optional[str] = Field(default=None, alias="NEWSAPI_API_KEY")
    semantic_scholar_key: Optional[str] = Field(default=None, alias="SEMANTIC_SCHOLAR_API_KEY")
    perplexity_key: Optional[str] = Field(default=None, alias="PERPLEXITY_API_KEY")
    tavily_key: Optional[str] = Field(default=None, alias="TAVILY_API_KEY")
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    google_cse_id: Optional[str] = Field(default=None, alias="GOOGLE_CSE_ID")


class PlannerConfig(BaseModel):
    default_plan: str = Field(
        "Coverage on climate, conflict, economy, and tech at global scale.",
        alias="HUMAN_DIARY_DEFAULT_PLAN",
    )
    regions: List[str] = Field(
        default_factory=lambda: ["americas", "emea", "apac"],
        alias="HUMAN_DIARY_REGIONS",
    )
    max_iterations: int = Field(12, alias="HUMAN_DIARY_MAX_ITERATIONS")


class RuntimeConfig(BaseModel):
    api: ApiConfig
    planner: PlannerConfig


@lru_cache(maxsize=1)
def load_runtime_config() -> RuntimeConfig:
    load_dotenv(override=False)
    api = ApiConfig()
    planner = PlannerConfig()
    return RuntimeConfig(api=api, planner=planner)
