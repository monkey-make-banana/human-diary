"""
Publish + memory agents to export entries and store feedback.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


class PublishAgent:
    def __init__(self, output_dir: Optional[Path] = None) -> None:
        self.output_dir = output_dir or Path("artifacts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def run(
        self,
        selection: Dict[str, Any],
        revisions: Iterable[Dict[str, Any]],
        sensemaking: Iterable[Dict[str, Any]],
        review: Any,
    ) -> Dict[str, Any]:
        revision_map = {revision.get("id"): revision for revision in revisions}
        winner = revision_map.get(selection.get("winner_id")) or next(iter(revision_map.values()), None)
        entry = _render_entry(winner, sensemaking)
        output_path = self.output_dir / f"entry-{selection.get('winner_id', 'draft')}.md"
        output_path.write_text(entry)
        return {
            "published_entry": entry,
            "publish_path": str(output_path),
            "publication_meta": {"review": review, "selection": selection},
        }


class MemoryAgent:
    def __init__(self, memory_path: Optional[Path] = None) -> None:
        self.memory_path = memory_path or Path(".cache/newsroom_memory.jsonl")
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)

    async def run(self, publication_payload: Dict[str, Any], planner_feedback: Any) -> Dict[str, Any]:
        frame = {
            "published_entry": publication_payload.get("published_entry"),
            "metadata": publication_payload.get("publication_meta"),
            "planner_feedback": planner_feedback,
        }
        with self.memory_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(frame) + "\n")
        return {"memory_write": str(self.memory_path)}


def _render_entry(revision: Optional[Dict[str, Any]], sensemaking: Iterable[Dict[str, Any]]) -> str:
    if not revision:
        return "No entry produced."
    bullets = "\n".join(
        f"- **{item.get('theme')}** ({item.get('impact')}/{item.get('uncertainty')}): {item.get('why_it_matters')}"
        for item in sensemaking
    )
    return (
        f"# {revision.get('lede', \"Humanity's Diary\")}\n\n"
        f"{revision.get('body', '')}\n\n"
        f"## Why it matters\n{bullets}\n"
    )
