# agents/retriever.py
"""
Retriever Agent — finds relevant documents using vector search.
Pure LangGraph node — no legacy AgentExecutor needed.
"""
import sys
sys.path.insert(0, ".")
from tools.retrieval_tool import search_documents

def retriever_node(state: dict, llm) -> dict:
    """Search documents for the given question."""
    print("\n[RETRIEVER] Searching documents...")
    question  = state["question"]
    retrieved = search_documents.invoke(question)
    print(f"[RETRIEVER] Found {len(retrieved)} chars of content")
    return {**state, "retrieved_docs": retrieved}
