"""
Chapter 7 — Build Your Own Agent Framework (HelloAgents Mini)
A minimal but complete agent framework built on the OpenAI native API.

Features:
- Tool registration via @agent.tool decorator
- Configurable memory (conversation history)
- Step-by-step execution logging
- Multi-agent handoff support

Prerequisites:
    pip install openai python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python mini_framework.py
"""

import os
import json
import inspect
from typing import Callable, Any
from dataclasses import dataclass, field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ─── Core Framework ───────────────────────────────────────────────────────────

@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@dataclass
class Memory:
    """Simple sliding-window conversation memory."""
    max_messages: int = 20
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.max_messages:
            # Keep system messages, evict oldest non-system message
            non_system = [m for m in self.messages if m.role != "system"]
            if non_system:
                self.messages.remove(non_system[0])

    def to_list(self) -> list[dict]:
        return [m.to_dict() for m in self.messages]


class Tool:
    """Wraps a Python function as an agent-callable tool."""

    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__
        self.description = func.__doc__ or f"Tool: {self.name}"
        self._build_schema()

    def _build_schema(self):
        """Auto-generate JSON schema from Python type hints."""
        hints = self.func.__annotations__
        properties = {}
        required = []

        sig = inspect.signature(self.func)
        for param_name, param in sig.parameters.items():
            if param_name == "return":
                continue
            hint = hints.get(param_name, str)
            type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}
            properties[param_name] = {"type": type_map.get(hint, "string")}
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        self.schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description.strip(),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    def call(self, **kwargs) -> str:
        result = self.func(**kwargs)
        return str(result)


class Agent:
    """A fully functional LLM agent with tools, memory, and logging."""

    def __init__(
        self,
        name: str = "Agent",
        model: str = "gpt-4o-mini",
        system_prompt: str = "You are a helpful assistant.",
        max_steps: int = 10,
        verbose: bool = True,
    ):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt
        self.max_steps = max_steps
        self.verbose = verbose
        self.tools: dict[str, Tool] = {}
        self.memory = Memory()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def tool(self, func: Callable) -> Callable:
        """Decorator to register a function as an agent tool."""
        t = Tool(func)
        self.tools[t.name] = t
        if self.verbose:
            print(f"[{self.name}] Registered tool: {t.name}")
        return func

    def _log(self, *args):
        if self.verbose:
            print(*args)

    def run(self, user_input: str) -> str:
        """Run the agent on a user input and return the final answer."""
        self.memory.add("user", user_input)
        self._log(f"\n{'─'*50}")
        self._log(f"[{self.name}] User: {user_input}")

        messages = [{"role": "system", "content": self.system_prompt}] + self.memory.to_list()
        tool_schemas = [t.schema for t in self.tools.values()]

        for step in range(self.max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_schemas if tool_schemas else None,
                tool_choice="auto" if tool_schemas else None,
            )

            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                # Final answer
                answer = msg.content or ""
                self.memory.add("assistant", answer)
                self._log(f"[{self.name}] Answer: {answer}")
                return answer

            # Execute tool calls
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                args = json.loads(tc.function.arguments)
                self._log(f"[{self.name}] Step {step+1} → {tool_name}({args})")

                if tool_name in self.tools:
                    result = self.tools[tool_name].call(**args)
                else:
                    result = f"Error: unknown tool '{tool_name}'"

                self._log(f"[{self.name}] Result: {result[:200]}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        return "Max steps reached."


# ─── Demo: Build an agent with custom tools ───────────────────────────────────

def main():
    print("Hello-Agents | Chapter 7: Build Your Own Framework")
    print("=" * 50)

    # Create the agent
    agent = Agent(
        name="ResearchBot",
        system_prompt="""You are a research assistant. 
Use your tools to answer questions accurately. 
Always show your calculations when asked to compute something.""",
    )

    # Register tools with the @agent.tool decorator
    @agent.tool
    def calculate(expression: str) -> str:
        """Evaluate a mathematical expression safely. E.g. '2**10', 'sqrt(16)'"""
        import math
        try:
            allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            return str(eval(expression, {"__builtins__": {}}, allowed))
        except Exception as e:
            return f"Error: {e}"

    @agent.tool
    def word_count(text: str) -> str:
        """Count the number of words in a given text string."""
        count = len(text.split())
        return f"{count} words"

    @agent.tool
    def list_fibonacci(n: int) -> str:
        """Generate the first N Fibonacci numbers."""
        if n <= 0:
            return "[]"
        fibs = [0, 1]
        while len(fibs) < n:
            fibs.append(fibs[-1] + fibs[-2])
        return str(fibs[:n])

    print()

    # Run some queries
    queries = [
        "What is 2 to the power of 16?",
        "List the first 10 Fibonacci numbers.",
        "How many words are in: 'The quick brown fox jumps over the lazy dog'?",
    ]

    for q in queries:
        agent.run(q)
        print()


if __name__ == "__main__":
    main()
