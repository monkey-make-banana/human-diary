# Humanity's Diary – Agentic Newsroom Stack

This package assembles the orchestration primitives described in the design brief:

- **BabyAGI** (via LangChain Experimental) handles planner⇄reviewer iterations that decide which regions/themes to cover.
- **LangGraph** routes state through retrieval, normalization, clustering, sense-making, writing, critique, and revision loops.
- **LangChain** tools tap **Semantic Scholar**, **Perplexity Sonar**, **OpenAI Web Search**, **SerpAPI**, and **NewsAPI.ai** for evidence, with provenance and dedupe rules baked in.
- Long-context summarizers, LaTeX-ready exporters, reviewer scoring, and publish + memory services mirror modern agentic research labs.

## Quick start

```bash
cd human_diary_pipeline
pip install -e .
cp .env.example .env  # provide API keys for OpenAI, SerpAPI, NewsAPI, SemanticScholar, Perplexity etc.
human-diary-newsroom --plan "Focus on climate resilience in coastal Asia"
```

The CLI spins up a LangGraph workflow built from modular nodes so you can stream state transitions (planner → retriever → writer) or run the end-to-end pipeline.

## Key directories

- `src/human_diary_pipeline/agents/`: planner/reviewer, retrieval/cleaning/clustering, sense-making, and writing agents.
- `src/human_diary_pipeline/adapters/`: wrappers for each external data source and provenance utilities.
- `src/human_diary_pipeline/graph/`: LangGraph definitions plus runtime instrumentation.
- `src/human_diary_pipeline/pipelines/`: high-level orchestration and CLI façade.
- `tests/`: smoke tests around the LangGraph build and config loading.

## Environment

Set the following variables (directly or via `.env`):

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SERPAPI_API_KEY=
NEWSAPI_API_KEY=
SEMANTIC_SCHOLAR_API_KEY=
PERPLEXITY_API_KEY=
```

Each adapter gracefully degrades when an API is missing so you can unit-test locally without network calls.

## Status

This is a composable scaffold meant to be expanded. Planner/critic heuristics, quality scoring prompts, toolchains, and guardrails are wired so you can plug in bespoke domain logic without rewriting the orchestration backbone.
