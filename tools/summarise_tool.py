# tools/summarise_tool.py
from langchain.tools import tool

@tool
def summarise_text(text: str) -> str:
    """
    Summarise a long text passage into 2-3 concise sentences.
    Input: full text passage to summarise
    Output: 2-3 sentence summary
    """
    if text.strip().startswith("[Document") and len(text.strip()) < 20:
        return "Error: pass full text, not a label like [Document 1]"
    sentences = text.replace("\n", " ").split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    summary   = ". ".join(sentences[:3])
    return summary + "." if summary else text[:300]
