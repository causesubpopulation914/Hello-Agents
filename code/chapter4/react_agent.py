"""
Chapter 4 — ReAct Agent from Scratch
Implements the ReAct (Reason + Act) paradigm: Thought → Action → Observation → loop.

Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
https://arxiv.org/abs/2210.03629

Prerequisites:
    pip install openai python-dotenv requests
    Add OPENAI_API_KEY to a .env file

Run:
    python react_agent.py
"""

import os
import json
import math
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Tools ────────────────────────────────────────────────────────────────────

def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Restrict to safe math operations
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def web_search(query: str) -> str:
    """Search Wikipedia for a given query and return a summary."""
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No summary found.")[:500]
        return f"No results found for '{query}'."
    except Exception as e:
        return f"Search failed: {e}"


def get_current_date() -> str:
    """Return the current date."""
    from datetime import datetime
    return datetime.now().strftime("%B %d, %Y")


# ─── Tool registry ────────────────────────────────────────────────────────────

TOOLS = {
    "calculator": calculator,
    "web_search": web_search,
    "get_current_date": get_current_date,
}

TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a math expression. Use Python syntax. Examples: '2 + 2', 'sqrt(144)', '3 ** 10'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The math expression to evaluate"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search Wikipedia for information about a topic. Use for factual questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get today's date.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

SYSTEM_PROMPT = """You are a ReAct agent. For each user question, you reason step-by-step and use tools when needed.

Follow this loop:
1. Thought: Reason about what to do next
2. Action: Call a tool if needed
3. Observation: Examine the tool result
4. Repeat until you have a final answer

When you have enough information, give the Final Answer directly."""


# ─── ReAct Loop ───────────────────────────────────────────────────────────────

def run_react_agent(question: str, max_steps: int = 10) -> str:
    """Run the ReAct loop for a given question."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_DESCRIPTIONS,
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message)

        # No tool call → final answer
        if not message.tool_calls:
            print(f"\n✅ Final Answer: {message.content}")
            return message.content

        # Process tool calls
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"\n[Step {step + 1}] 🔧 Tool: {tool_name}")
            print(f"         Args: {tool_args}")

            if tool_name in TOOLS:
                # Call with args if function accepts them
                func = TOOLS[tool_name]
                try:
                    import inspect
                    sig = inspect.signature(func)
                    observation = func(**tool_args) if sig.parameters else func()
                except Exception as e:
                    observation = f"Tool error: {e}"
            else:
                observation = f"Unknown tool: {tool_name}"

            print(f"         Result: {observation[:200]}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(observation),
            })

    return "Max steps reached without a final answer."


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    questions = [
        "What is 17 multiplied by 38, then divided by 13? Round to 2 decimal places.",
        "Who invented the transformer architecture in machine learning?",
        "What is today's date, and what day of the week is it?",
    ]

    for q in questions:
        run_react_agent(q)
        print()
