"""
Factory helpers to instantiate adapters based on runtime config.
"""

from __future__ import annotations

from typing import Dict, List

from ..config import RuntimeConfig
from .base import SourceAdapter
from .newsapi import NewsApiAdapter
from .openai_web import OpenAIWebSearchAdapter
from .perplexity import PerplexitySonarAdapter
from .semantic_scholar import SemanticScholarAdapter
from .serpapi import SerpApiNewsAdapter


def build_adapter_suite(config: RuntimeConfig) -> Dict[str, SourceAdapter]:
    api = config.api
    adapters = {
        "semantic_scholar": SemanticScholarAdapter(api.semantic_scholar_key),
        "perplexity": PerplexitySonarAdapter(api.perplexity_key),
        "serpapi": SerpApiNewsAdapter(api.serpapi_api_key),
        "newsapi": NewsApiAdapter(api.newsapi_key),
        "openai_web": OpenAIWebSearchAdapter(api.openai_api_key),
    }
    return adapters


def adapter_list(config: RuntimeConfig) -> List[SourceAdapter]:
    return list(build_adapter_suite(config).values())
