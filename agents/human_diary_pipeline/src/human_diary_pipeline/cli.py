"""
Command line entrypoint for running the newsroom LangGraph pipeline.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any, Dict

from .config import load_runtime_config
from .pipelines.newsroom import build_default_newsroom


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Humanity's Diary agentic newsroom runner.")
    parser.add_argument(
        "--plan",
        type=str,
        default=None,
        help="Optional planner directive overriding the PlannerConfig.default_plan value.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional file path to dump the final state snapshot (JSON).",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream state updates as the LangGraph executes.",
    )
    return parser.parse_args()


async def _run_async(plan: str | None, output: Path | None, stream: bool) -> Dict[str, Any]:
    config = load_runtime_config()
    if plan:
        planner_directive = plan
    else:
        planner_directive = config.planner.default_plan

    workflow = build_default_newsroom(config, planner_directive=planner_directive)
    if stream:
        final_state: Dict[str, Any] = {}
        async for event in workflow.astream({}):
            node = event.get("node")
            if node:
                print(f"[node:{node}]")  # noqa: T201 - CLI feedback
            if "state" in event:
                final_state = event["state"]
        result = final_state
    else:
        result = await workflow.ainvoke({})

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2))

    return result


def main() -> None:
    args = _parse_args()
    asyncio.run(_run_async(plan=args.plan, output=args.output, stream=args.stream))


if __name__ == "__main__":
    main()
