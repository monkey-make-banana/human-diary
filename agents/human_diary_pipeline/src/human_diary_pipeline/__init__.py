"""
Humanity's Diary agentic newsroom stack.

This module glues together BabyAGI planners, LangChain tools, LangGraph workflows,
and bespoke adapters for citation-aware summarization pipelines.
"""

from .pipelines.newsroom import build_default_newsroom

__all__ = ["build_default_newsroom"]
