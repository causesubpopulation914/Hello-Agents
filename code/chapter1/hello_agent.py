"""
Chapter 1 — Hello, Agent!
Your very first LLM-powered agent in under 30 lines.

Prerequisites:
    pip install openai python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python hello_agent.py
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant. 
Answer clearly and concisely."""

def chat(user_message: str, history: list[dict]) -> str:
    """Send a message and get a response, maintaining conversation history."""
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
    )

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message


def main():
    print("Hello-Agents | Chapter 1: Your First Agent")
    print("=" * 45)
    print("Type 'quit' to exit\n")

    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        response = chat(user_input, history)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
