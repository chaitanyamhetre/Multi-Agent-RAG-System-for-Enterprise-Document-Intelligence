# src/graph.py
"""
LangGraph Multi-Agent Orchestration.

Graph structure:
  START → retriever_node → analyst_node → synthesiser_node → END

State accumulates:
  question, retrieved_docs, analyst_facts, final_answer
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import sys
sys.path.insert(0, ".")

from agents.retriever   import retriever_node
from agents.analyst     import analyst_node
from agents.synthesiser import synthesiser_node

# ── State ─────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    question:       str
    retrieved_docs: str
    analyst_facts:  str
    final_answer:   str

# ── Build graph ───────────────────────────────────────────────────────────
def build_graph(llm):
    graph = StateGraph(AgentState)

    graph.add_node("retriever",
                   lambda state: retriever_node(state, llm))
    graph.add_node("analyst",
                   lambda state: analyst_node(state, llm))
    graph.add_node("synthesiser",
                   lambda state: synthesiser_node(state, llm))

    graph.add_edge(START,         "retriever")
    graph.add_edge("retriever",   "analyst")
    graph.add_edge("analyst",     "synthesiser")
    graph.add_edge("synthesiser", END)

    return graph.compile()

def run_pipeline(question: str, llm) -> dict:
    """Run full multi-agent pipeline."""
    pipeline = build_graph(llm)

    initial_state = AgentState(
        question       = question,
        retrieved_docs = "",
        analyst_facts  = "",
        final_answer   = ""
    )

    final_state = pipeline.invoke(initial_state)
    return {
        "question":       question,
        "retrieved_docs": final_state["retrieved_docs"],
        "analyst_facts":  final_state["analyst_facts"],
        "final_answer":   final_state["final_answer"]
    }
