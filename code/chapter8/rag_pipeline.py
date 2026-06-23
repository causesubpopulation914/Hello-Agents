"""
Chapter 8 — RAG Pipeline from Scratch
Retrieval-Augmented Generation using ChromaDB + OpenAI Embeddings.

This implements the full RAG loop:
1. Ingest documents → chunk → embed → store in vector DB
2. Query → embed → retrieve top-k chunks → augment prompt → generate answer

Prerequisites:
    pip install openai chromadb python-dotenv
    Add OPENAI_API_KEY to a .env file

Run:
    python rag_pipeline.py
"""

import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("ChromaDB not installed. Run: pip install chromadb")
    print("Falling back to in-memory similarity search.\n")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Sample Knowledge Base ────────────────────────────────────────────────────

DOCUMENTS = [
    {
        "id": "doc1",
        "title": "What is an Agent?",
        "content": """An AI agent is a system that perceives its environment, reasons about it, 
and takes actions to achieve goals. Unlike a simple chatbot, an agent can use tools, 
remember past interactions, plan multi-step tasks, and adapt its behavior based on feedback. 
The key components of an agent are: perception (input), reasoning (LLM), memory, tools, and action.""",
    },
    {
        "id": "doc2",
        "title": "ReAct Paradigm",
        "content": """ReAct (Reason + Act) is a prompting paradigm where the agent interleaves 
reasoning traces and actions. The loop is: Thought (reason about the next step) → Action (call a tool) 
→ Observation (read the result) → repeat. This approach was introduced in the paper 
'ReAct: Synergizing Reasoning and Acting in Language Models' (Yao et al., 2022).""",
    },
    {
        "id": "doc3",
        "title": "RAG (Retrieval-Augmented Generation)",
        "content": """RAG combines a retrieval system with a language model. When a user asks a question, 
the system retrieves relevant documents from a knowledge base, then passes them as context to the LLM 
to generate a grounded answer. This reduces hallucinations and allows the model to access up-to-date 
information without fine-tuning. Key components: embedding model, vector database, retriever, generator.""",
    },
    {
        "id": "doc4",
        "title": "MCP Protocol",
        "content": """Model Context Protocol (MCP) is an open standard that defines how AI models 
communicate with external tools and services. MCP standardizes the interface between agents and tools, 
making it easier to build composable, interoperable agent systems. It defines message formats, 
tool schemas, and communication patterns for agent-to-tool and agent-to-agent interactions.""",
    },
    {
        "id": "doc5",
        "title": "Agent Memory Systems",
        "content": """Agents use different types of memory: (1) Working memory — the current context 
window, holding recent conversation turns. (2) Episodic memory — past interactions stored externally, 
retrieved when needed. (3) Semantic memory — factual knowledge in a vector database. 
(4) Procedural memory — learned skills and tool-use patterns. Effective memory management is critical 
for long-running agents.""",
    },
]


# ─── Text Chunking ────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


# ─── Embedding ────────────────────────────────────────────────────────────────

def embed(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using OpenAI's text-embedding-3-small model."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [item.embedding for item in response.data]


# ─── In-memory fallback retriever ─────────────────────────────────────────────

class SimpleRetriever:
    """Cosine similarity retrieval without ChromaDB (fallback)."""

    def __init__(self):
        self.chunks: list[str] = []
        self.embeddings: list[list[float]] = []
        self.metadata: list[dict] = []

    def add(self, chunks: list[str], meta: list[dict]):
        vecs = embed(chunks)
        self.chunks.extend(chunks)
        self.embeddings.extend(vecs)
        self.metadata.extend(meta)
        print(f"  Indexed {len(chunks)} chunks")

    def query(self, question: str, k: int = 3) -> list[dict]:
        import math

        q_vec = embed([question])[0]

        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            na = math.sqrt(sum(x**2 for x in a))
            nb = math.sqrt(sum(x**2 for x in b))
            return dot / (na * nb) if na and nb else 0

        scores = [(cosine(q_vec, ev), i) for i, ev in enumerate(self.embeddings)]
        scores.sort(reverse=True)
        return [{"text": self.chunks[i], "meta": self.metadata[i]} for _, i in scores[:k]]


# ─── RAG Pipeline ─────────────────────────────────────────────────────────────

class RAGPipeline:
    def __init__(self):
        if CHROMA_AVAILABLE:
            chroma_client = chromadb.Client()
            self.collection = chroma_client.create_collection(
                name="hello_agents_kb",
                get_or_create=True,
            )
            self.use_chroma = True
        else:
            self.retriever = SimpleRetriever()
            self.use_chroma = False

    def ingest(self, documents: list[dict]):
        """Chunk, embed, and store all documents."""
        print("\n📥 Ingesting documents...")
        for doc in documents:
            chunks = chunk_text(doc["content"])
            meta = [{"title": doc["title"], "doc_id": doc["id"]} for _ in chunks]

            if self.use_chroma:
                vecs = embed(chunks)
                ids = [str(uuid.uuid4()) for _ in chunks]
                self.collection.add(
                    ids=ids,
                    embeddings=vecs,
                    documents=chunks,
                    metadatas=meta,
                )
                print(f"  Indexed '{doc['title']}' → {len(chunks)} chunks")
            else:
                self.retriever.add(chunks, meta)
                print(f"  Indexed '{doc['title']}'")

        print(f"✅ Knowledge base ready ({len(documents)} documents)\n")

    def retrieve(self, question: str, k: int = 3) -> list[dict]:
        """Find the most relevant chunks for a question."""
        if self.use_chroma:
            q_vec = embed([question])[0]
            results = self.collection.query(
                query_embeddings=[q_vec],
                n_results=k,
            )
            return [
                {"text": doc, "meta": meta}
                for doc, meta in zip(results["documents"][0], results["metadatas"][0])
            ]
        else:
            return self.retriever.query(question, k=k)

    def generate(self, question: str, context_chunks: list[dict]) -> str:
        """Generate an answer using retrieved context."""
        context = "\n\n".join(
            f"[Source: {c['meta']['title']}]\n{c['text']}"
            for c in context_chunks
        )

        prompt = f"""Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise, helpful assistant that only uses the provided context."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    def ask(self, question: str) -> str:
        """Full RAG pipeline: retrieve → generate → return answer."""
        print(f"❓ Question: {question}")

        chunks = self.retrieve(question, k=3)
        print(f"📚 Retrieved {len(chunks)} relevant chunks:")
        for c in chunks:
            print(f"   • {c['meta']['title']}: {c['text'][:80]}...")

        answer = self.generate(question, chunks)
        print(f"\n💡 Answer: {answer}\n")
        return answer


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Hello-Agents | Chapter 8: RAG Pipeline")
    print("=" * 45)

    rag = RAGPipeline()
    rag.ingest(DOCUMENTS)

    questions = [
        "What is the ReAct paradigm and how does it work?",
        "How do agents handle memory?",
        "What is MCP and why is it useful?",
        "How does RAG reduce hallucinations?",
    ]

    print("─" * 45)
    for q in questions:
        rag.ask(q)
        print("─" * 45)
