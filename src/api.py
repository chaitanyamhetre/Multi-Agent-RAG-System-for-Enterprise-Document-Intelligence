# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time, os, sys
sys.path.insert(0, ".")

app = FastAPI(
    title="Multi-Agent RAG Enterprise API",
    description="""
A production-ready Multi-Agent RAG system built with LangGraph.

## Architecture
Three specialised agents collaborate to answer questions:
- **Retriever Agent** — semantic vector search over document corpus
- **Analyst Agent** — extracts key facts from retrieved documents
- **Synthesiser Agent** — generates final grounded answer

## Tool Interface
Follows the Model Context Protocol (MCP) tool-calling pattern.
    """,
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class AgentPipelineResponse(BaseModel):
    question:      str
    final_answer:  str
    analyst_facts: str
    success:       bool
    time_sec:      float
    pipeline:      str = "retriever → analyst → synthesiser"

class HealthResponse(BaseModel):
    status:     str
    model:      str
    index_size: int
    agents:     list

from langchain_groq import ChatGroq
from src.graph import run_pipeline
from tools.retrieval_tool import index

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Set GROQ_API_KEY environment variable before starting")

_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=512
)

@app.get("/")
def root():
    return {"name": "Multi-Agent RAG Enterprise API", "version": "1.0.0"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy", model="llama-3.1-8b-instant",
        index_size=index.ntotal,
        agents=["retriever", "analyst", "synthesiser"]
    )

@app.post("/ask", response_model=AgentPipelineResponse)
def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question too long")
    t0      = time.perf_counter()
    result  = run_pipeline(request.question, _llm)
    elapsed = round(time.perf_counter() - t0, 3)
    success = "cannot be determined" not in result["final_answer"].lower()
    return AgentPipelineResponse(
        question=request.question,
        final_answer=result["final_answer"],
        analyst_facts=result["analyst_facts"],
        success=success,
        time_sec=elapsed
    )
