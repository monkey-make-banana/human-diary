"""
Utility helpers for creating LangChain LLM instances.
"""

from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ..config import RuntimeConfig


class LLMFactory:
    def __init__(self, config: RuntimeConfig) -> None:
        self.config = config

    def planner_model(self) -> BaseChatModel:
        if self.config.api.anthropic_api_key:
            return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2)
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    def writer_model(self) -> BaseChatModel:
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    def critic_model(self) -> BaseChatModel:
        if self.config.api.anthropic_api_key:
            return ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.1)
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(model="text-embedding-3-large")
