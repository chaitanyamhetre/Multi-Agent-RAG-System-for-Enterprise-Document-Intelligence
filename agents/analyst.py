# agents/analyst.py
"""
Analyst Agent — extracts key facts from retrieved documents.
Uses LLM directly to analyse content.
"""
from langchain_core.messages import HumanMessage, SystemMessage

ANALYST_SYSTEM = """You are a Document Analyst. 
Extract the key facts from the provided documents that are 
relevant to answering the question.
Return a bullet-point list of key facts only.
Be concise — max 5 bullet points."""

def analyst_node(state: dict, llm) -> dict:
    """Extract key facts from retrieved documents."""
    print("\n[ANALYST] Extracting key facts...")
    
    prompt = f"""Question: {state["question"]}

Retrieved Documents:
{state["retrieved_docs"][:1500]}

Extract the key facts needed to answer this question."""

    messages = [
        SystemMessage(content=ANALYST_SYSTEM),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    facts    = response.content.strip()
    print(f"[ANALYST] Extracted facts: {facts[:100]}...")
    return {**state, "analyst_facts": facts}
