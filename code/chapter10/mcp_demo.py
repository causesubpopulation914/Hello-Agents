"""
Chapter 10 — Agent Communication Protocols: MCP Demo
Simulates the Model Context Protocol (MCP) pattern for tool communication.

This demo implements a simplified MCP-style server and client:
- MCP Server: exposes tools via a standardized JSON interface
- MCP Client (Agent): discovers and calls tools through the protocol

In production, MCP uses stdio or HTTP transport. This demo uses in-process
function calls to illustrate the protocol structure clearly.

Learn more: https://modelcontextprotocol.io

Prerequisites:
    pip install openai python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python mcp_demo.py
"""

import os
import json
import uuid
import math
from dataclasses import dataclass, field
from typing import Any, Callable
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ─── MCP Protocol Types ───────────────────────────────────────────────────────

@dataclass
class MCPToolSchema:
    """Describes a tool exposed by an MCP server."""
    name: str
    description: str
    input_schema: dict  # JSON Schema for the input


@dataclass
class MCPRequest:
    """A tool call request from the client."""
    request_id: str
    tool_name: str
    arguments: dict


@dataclass
class MCPResponse:
    """A tool call response from the server."""
    request_id: str
    content: list[dict]  # [{type: "text", text: "..."}, ...]
    is_error: bool = False


# ─── MCP Server ───────────────────────────────────────────────────────────────

class MCPServer:
    """
    A simplified MCP server that exposes tools via the protocol.
    In production, this would run as a separate process.
    """

    def __init__(self, name: str):
        self.name = name
        self._tools: dict[str, tuple[MCPToolSchema, Callable]] = {}

    def register_tool(self, schema: MCPToolSchema, func: Callable):
        self._tools[schema.name] = (schema, func)
        print(f"[MCPServer:{self.name}] Registered tool: {schema.name}")

    def list_tools(self) -> list[MCPToolSchema]:
        """Protocol: list available tools."""
        return [schema for schema, _ in self._tools.values()]

    def call_tool(self, request: MCPRequest) -> MCPResponse:
        """Protocol: execute a tool call and return the result."""
        if request.tool_name not in self._tools:
            return MCPResponse(
                request_id=request.request_id,
                content=[{"type": "text", "text": f"Unknown tool: {request.tool_name}"}],
                is_error=True,
            )

        schema, func = self._tools[request.tool_name]
        try:
            result = func(**request.arguments)
            return MCPResponse(
                request_id=request.request_id,
                content=[{"type": "text", "text": str(result)}],
            )
        except Exception as e:
            return MCPResponse(
                request_id=request.request_id,
                content=[{"type": "text", "text": f"Error: {e}"}],
                is_error=True,
            )


# ─── MCP Client (Agent) ───────────────────────────────────────────────────────

class MCPAgent:
    """
    An LLM agent that communicates with MCP servers to use tools.
    Discovers tools at runtime via the MCP protocol.
    """

    def __init__(self, servers: list[MCPServer]):
        self.servers = {s.name: s for s in servers}
        self.tool_map: dict[str, tuple[str, MCPToolSchema]] = {}  # tool_name → (server_name, schema)
        self._discover_tools()

    def _discover_tools(self):
        """Discover all tools from all connected MCP servers."""
        print("\n[MCPAgent] Discovering tools from servers...")
        for server_name, server in self.servers.items():
            for schema in server.list_tools():
                self.tool_map[schema.name] = (server_name, schema)
                print(f"  ✓ {server_name}.{schema.name}")

    def _schemas_for_openai(self) -> list[dict]:
        """Convert MCP tool schemas to OpenAI function-calling format."""
        tools = []
        for tool_name, (_, schema) in self.tool_map.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": schema.description,
                    "parameters": schema.input_schema,
                },
            })
        return tools

    def _call_tool(self, tool_name: str, arguments: dict) -> str:
        """Route a tool call to the appropriate MCP server."""
        if tool_name not in self.tool_map:
            return f"Tool not found: {tool_name}"

        server_name, _ = self.tool_map[tool_name]
        server = self.servers[server_name]

        request = MCPRequest(
            request_id=str(uuid.uuid4()),
            tool_name=tool_name,
            arguments=arguments,
        )

        response = server.call_tool(request)
        text = " ".join(c["text"] for c in response.content if c["type"] == "text")
        return f"[ERROR] {text}" if response.is_error else text

    def run(self, question: str) -> str:
        """Run the agent using MCP tools."""
        print(f"\n{'='*60}")
        print(f"[MCPAgent] Question: {question}")
        print(f"{'='*60}")

        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to tools via MCP servers."},
            {"role": "user", "content": question},
        ]
        tool_schemas = self._schemas_for_openai()

        for step in range(10):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tool_schemas,
                tool_choice="auto",
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                print(f"\n[MCPAgent] ✅ Answer: {msg.content}")
                return msg.content

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                print(f"\n[MCPAgent] Step {step+1} → {tc.function.name}({args})")
                result = self._call_tool(tc.function.name, args)
                print(f"[MCPAgent] Result: {result[:200]}")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

        return "Max steps reached."


# ─── Build MCP Servers ────────────────────────────────────────────────────────

def build_math_server() -> MCPServer:
    server = MCPServer("math-server")

    server.register_tool(
        MCPToolSchema(
            name="calculate",
            description="Evaluate a mathematical expression. Supports standard math operations and functions.",
            input_schema={
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "Math expression to evaluate"}},
                "required": ["expression"],
            },
        ),
        lambda expression: eval(expression, {"__builtins__": {}}, {k: v for k, v in math.__dict__.items() if not k.startswith("__")}),
    )

    server.register_tool(
        MCPToolSchema(
            name="convert_units",
            description="Convert between common units. E.g. miles to km, Fahrenheit to Celsius.",
            input_schema={
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "from_unit": {"type": "string"},
                    "to_unit": {"type": "string"},
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        ),
        lambda value, from_unit, to_unit: _convert(value, from_unit, to_unit),
    )

    return server


def build_text_server() -> MCPServer:
    server = MCPServer("text-server")

    server.register_tool(
        MCPToolSchema(
            name="word_count",
            description="Count the number of words in a text.",
            input_schema={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        ),
        lambda text: f"{len(text.split())} words",
    )

    server.register_tool(
        MCPToolSchema(
            name="reverse_text",
            description="Reverse the characters in a string.",
            input_schema={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        ),
        lambda text: text[::-1],
    )

    return server


def _convert(value: float, from_unit: str, to_unit: str) -> str:
    conversions = {
        ("miles", "km"): lambda v: v * 1.60934,
        ("km", "miles"): lambda v: v / 1.60934,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
        ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("kg", "lbs"): lambda v: v * 2.20462,
        ("lbs", "kg"): lambda v: v / 2.20462,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = round(conversions[key](value), 4)
        return f"{value} {from_unit} = {result} {to_unit}"
    return f"Conversion from {from_unit} to {to_unit} not supported."


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Hello-Agents | Chapter 10: MCP Protocol Demo")
    print("=" * 50)

    math_server = build_math_server()
    text_server = build_text_server()
    agent = MCPAgent(servers=[math_server, text_server])

    questions = [
        "What is the square root of 1764, and how many words is this sentence?",
        "Convert 100 miles to kilometers, then calculate the square of that result.",
        "What is 98.6 degrees Fahrenheit in Celsius?",
    ]

    for q in questions:
        agent.run(q)
        print()
