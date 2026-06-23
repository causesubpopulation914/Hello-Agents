"""
Chapter 4 — Plan-and-Solve Agent
Implements the Plan-and-Solve paradigm: first create a plan, then execute each step.

Paper: "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning"
https://arxiv.org/abs/2305.04091

Prerequisites:
    pip install openai python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python plan_and_solve.py
"""

import os
import json
import math
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─── Planner ──────────────────────────────────────────────────────────────────

PLANNER_PROMPT = """You are a planning assistant. Given a complex question, break it down into 
clear, numbered steps. Return ONLY a JSON array of step strings.

Example output:
["Step 1: Identify the key variables", "Step 2: Look up relevant facts", "Step 3: Calculate the answer"]

Question: {question}
"""

def create_plan(question: str) -> list[str]:
    """Break a question into a list of executable steps."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PLANNER_PROMPT.format(question=question)}],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    parsed = json.loads(content)
    # Handle various JSON shapes the model might return
    if isinstance(parsed, list):
        return parsed
    for key in ("steps", "plan", "items"):
        if key in parsed and isinstance(parsed[key], list):
            return parsed[key]
    return list(parsed.values())[0] if parsed else []


# ─── Solver ───────────────────────────────────────────────────────────────────

SOLVER_PROMPT = """You are solving a problem step by step.

Original question: {question}

Plan:
{plan}

Now execute each step carefully and provide the final answer.
Show your work for each step."""

def solve(question: str, plan: list[str]) -> str:
    """Execute the plan and produce a final answer."""
    plan_text = "\n".join(plan)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": SOLVER_PROMPT.format(question=question, plan=plan_text)
        }],
    )
    return response.choices[0].message.content


# ─── Plan-and-Solve Agent ─────────────────────────────────────────────────────

def plan_and_solve(question: str) -> str:
    """Full Plan-and-Solve pipeline."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    # Phase 1: Plan
    print("\n📋 Phase 1: Planning...")
    plan = create_plan(question)
    for step in plan:
        print(f"  {step}")

    # Phase 2: Solve
    print("\n⚙️  Phase 2: Solving...")
    answer = solve(question, plan)
    print(f"\n✅ Answer:\n{answer}")

    return answer


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Hello-Agents | Chapter 4: Plan-and-Solve Agent")

    questions = [
        "If a train travels at 120 km/h and needs to cover 450 km, how long will the journey take? Convert your answer to hours and minutes.",
        "Explain the key differences between RAG and fine-tuning for adapting LLMs to domain-specific tasks.",
    ]

    for q in questions:
        plan_and_solve(q)
        print()
