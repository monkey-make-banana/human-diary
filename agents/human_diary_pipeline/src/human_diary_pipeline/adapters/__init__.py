"""
Adapters for third-party data sources.
"""

from .newsapi import NewsApiAdapter
from .openai_web import OpenAIWebSearchAdapter
from .perplexity import PerplexitySonarAdapter
from .semantic_scholar import SemanticScholarAdapter
from .serpapi import SerpApiNewsAdapter

__all__ = [
    "NewsApiAdapter",
    "OpenAIWebSearchAdapter",
    "PerplexitySonarAdapter",
    "SemanticScholarAdapter",
    "SerpApiNewsAdapter",
]
