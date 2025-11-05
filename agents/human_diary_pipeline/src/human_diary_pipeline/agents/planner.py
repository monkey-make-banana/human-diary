"""
Planner ↔ reviewer loop backed by BabyAGI.
"""

from __future__ import annotations

from typing import Dict, List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_experimental.agents.baby_agi import BabyAGI
from langchain_community.vectorstores import DocArrayInMemorySearch

from ..config import RuntimeConfig
from .llm import LLMFactory


def _task_execution_chain(factory: LLMFactory) -> LLMChain:
    prompt = PromptTemplate(
        template=(
            "You are the Humanity's Diary planner. Objective: {objective}.\n"
            "Current task: {task}.\n"
            "Respond with a JSON bullet of the form "
            '{"title": "...", "region": "...", "theme": "...", "angle": "..."}'
        ),
        input_variables=["objective", "task"],
    )
    return LLMChain(llm=factory.planner_model(), prompt=prompt, verbose=False)


class PlannerReviewerLoop:
    def __init__(self, config: RuntimeConfig, factory: LLMFactory) -> None:
        self.config = config
        self.factory = factory
        embeddings = factory.embeddings()
        self.vectorstore = DocArrayInMemorySearch.from_texts(
            ["Humanity's Diary anchor memory."],
            embedding=embeddings,
        )
        self._baby_agi = BabyAGI.from_llm(
            llm=factory.planner_model(),
            vectorstore=self.vectorstore,
            task_execution_chain=_task_execution_chain(factory),
            verbose=False,
            max_iterations=config.planner.max_iterations,
        )
        review_prompt = PromptTemplate(
            template=(
                "You are the Humanity's Diary reviewer.\n"
                "Objective: {objective}\nPlan candidates:\n{plan}\n\n"
                "Return critique JSON with keys `balance` (0-1), `coverage_notes`, `risks`."
            ),
            input_variables=["objective", "plan"],
        )
        self.review_chain = LLMChain(
            llm=factory.critic_model(),
            prompt=review_prompt,
            verbose=False,
        )

    async def run(self, directive: str) -> Dict[str, List[Dict[str, str]]]:
        result = await self._baby_agi.acall({"objective": directive})
        task_list = result.get("task_list") or result.get("tasks") or []
        plan_lines = []
        structured_tasks: List[Dict[str, str]] = []
        for line in task_list:
            plan_lines.append(line if isinstance(line, str) else str(line))
            if isinstance(line, dict):
                structured_tasks.append(line)
        review = await self.review_chain.apredict(objective=directive, plan="\n".join(plan_lines))
        return {
            "planner_directive": directive,
            "tasks": structured_tasks or task_list,
            "review": review,
        }
