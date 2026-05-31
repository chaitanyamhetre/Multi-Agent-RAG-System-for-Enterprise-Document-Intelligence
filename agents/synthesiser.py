# agents/synthesiser.py
"""
Synthesiser Agent — combines retrieved docs and facts 
into a final coherent answer.
"""
from langchain_core.messages import HumanMessage, SystemMessage

SYNTHESISER_SYSTEM = """You are an Answer Synthesis Agent.
Combine the retrieved documents and extracted facts into 
a clear, accurate, concise final answer.
Rules:
- Base answer ONLY on provided context
- Be concise — 2-4 sentences maximum  
- If context is insufficient, say so clearly
- Do not hallucinate"""

def synthesiser_node(state: dict, llm) -> dict:
    """Generate final answer from retrieved docs and facts."""
    print("\n[SYNTHESISER] Generating final answer...")

    prompt = f"""Question: {state["question"]}

Retrieved Documents:
{state["retrieved_docs"][:1000]}

Key Facts:
{state["analyst_facts"][:500]}

Provide a clear and accurate answer in 2-4 sentences."""

    messages = [
        SystemMessage(content=SYNTHESISER_SYSTEM),
        HumanMessage(content=prompt)
    ]
    response     = llm.invoke(messages)
    final_answer = response.content.strip()
    print(f"[SYNTHESISER] Answer: {final_answer[:100]}...")
    return {**state, "final_answer": final_answer}
