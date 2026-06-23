"""
Chapter 4 — Reflection Agent
The agent generates an answer, then critiques and improves it iteratively.

Reflection is a powerful self-improvement loop:
1. Generate an initial answer
2. Reflect: critique the answer for errors, gaps, or improvements
3. Revise: produce a better answer based on the critique
4. Repeat until the answer is satisfactory

Prerequisites:
    pip install openai python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python reflection_agent.py
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


GENERATOR_PROMPT = "You are an expert assistant. Answer the following question thoroughly and accurately."

CRITIC_PROMPT = """You are a critical reviewer. Evaluate the following answer to the question below.

Question: {question}
Answer: {answer}

Provide a structured critique:
1. What is CORRECT or well-explained?
2. What is MISSING, INCOMPLETE, or could be improved?
3. Are there any ERRORS or inaccuracies?
4. Give a score from 1-10 (10 = perfect, no improvements needed).

If the score is 8 or higher, end with: VERDICT: SATISFACTORY
Otherwise end with: VERDICT: NEEDS_IMPROVEMENT"""

REVISER_PROMPT = """You are an expert assistant. Improve the following answer based on the critique provided.

Question: {question}
Previous Answer: {answer}
Critique: {critique}

Write an improved, comprehensive answer that addresses all the critique points."""


def generate(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": GENERATOR_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


def reflect(question: str, answer: str) -> tuple[str, bool]:
    """Critique the answer. Returns (critique, is_satisfactory)."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": CRITIC_PROMPT.format(question=question, answer=answer),
        }],
    )
    critique = response.choices[0].message.content
    is_satisfactory = "VERDICT: SATISFACTORY" in critique
    return critique, is_satisfactory


def revise(question: str, answer: str, critique: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": REVISER_PROMPT.format(question=question, answer=answer, critique=critique),
        }],
    )
    return response.choices[0].message.content


def reflection_agent(question: str, max_iterations: int = 3) -> str:
    """Run the Reflection loop."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    # Step 1: Initial generation
    print("\n[Iteration 1] Generating initial answer...")
    answer = generate(question)
    print(f"Answer preview: {answer[:150]}...")

    for i in range(max_iterations):
        # Step 2: Reflect
        print(f"\n[Iteration {i+1}] Reflecting...")
        critique, is_satisfactory = reflect(question, answer)
        print(f"Critique preview: {critique[:200]}...")

        if is_satisfactory:
            print(f"\n✅ Answer is satisfactory after {i+1} iteration(s).")
            break

        if i < max_iterations - 1:
            # Step 3: Revise
            print(f"\n[Iteration {i+2}] Revising...")
            answer = revise(question, answer, critique)
            print(f"Revised answer preview: {answer[:150]}...")
        else:
            print(f"\n⚠️  Max iterations reached. Returning best answer.")

    print(f"\n📄 Final Answer:\n{answer}\n")
    return answer


if __name__ == "__main__":
    print("Hello-Agents | Chapter 4: Reflection Agent")

    questions = [
        "Explain the trade-offs between using RAG vs fine-tuning for adapting an LLM to a specialized domain.",
        "What are the main challenges in building reliable multi-agent systems?",
    ]

    for q in questions:
        reflection_agent(q)
