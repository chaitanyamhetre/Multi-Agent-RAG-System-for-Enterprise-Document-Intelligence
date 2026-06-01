# Multi-Agent RAG System for Enterprise Document Intelligence

A production-ready multi-agent RAG system built with LangGraph, where three
specialised agents collaborate to answer questions over a document knowledge base.
Deployed as a REST API with FastAPI and containerised with Docker.

---

## Architecture

```
User Query
        ↓
FastAPI REST Endpoint (POST /ask)
        ↓
LangGraph Orchestrator
        ↓
┌─────────────────────────────────────────┐
│            Retriever Agent              │
│  → semantic vector search (FAISS)       │
│  → returns top-3 relevant passages      │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│             Analyst Agent               │
│  → extracts key facts from documents    │
│  → bullet-point fact list               │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           Synthesiser Agent             │
│  → combines docs + facts                │
│  → generates final grounded answer      │
└─────────────────────────────────────────┘
                  ↓
            JSON Response
```

---

## Why Multi-Agent?

Single-agent RAG systems retrieve and answer in one step — which works for
simple questions but degrades on complex ones requiring reasoning, fact
extraction, or multi-step synthesis. Specialised agents each own one
responsibility:

| Agent | Responsibility | Why separate |
|---|---|---|
| Retriever | Find relevant documents | Optimised for recall, not reasoning |
| Analyst | Extract key facts | Reduces noise before synthesis |
| Synthesiser | Generate final answer | Focused on coherence and accuracy |

This separation of concerns mirrors production multi-agent architectures
at scale and produces measurably better results than single-agent pipelines.

---

## MCP Tool Interface Pattern

Each tool follows the Model Context Protocol (MCP) tool-calling pattern —
a standardised interface where tools expose a typed input schema and
structured output the agents reason over.

```python
@tool
def search_documents(query: str) -> str:
    """
    Search the document knowledge base for relevant passages.
    Input: natural language search query
    Output: top 3 relevant document passages
    """
```

---

## Evaluation Results

Evaluated on 30 MS MARCO QA pairs:

| Metric | Value |
|---|---|
| Answer accuracy (keyword match) | **40.0%** |
| Success rate (valid final answer) | **100.0%** |
| Avg response time per query | 7.80s |
| Total evaluation time | 234.1s |

---

## Dataset

**MS MARCO** — Microsoft Machine Reading Comprehension
- Source: `microsoft/ms_marco` v1.1 via HuggingFace Datasets
- Subset: 500 documents, 491 QA pairs
- Domain: diverse general-purpose documents

---

## API Endpoints

### Start the server
```bash
export GROQ_API_KEY=your_key_here
uvicorn src.api:app --reload
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/health` | Health check — model, index size, agents |
| POST | `/ask` | Run multi-agent pipeline |
| GET | `/docs` | Auto-generated Swagger UI |

### Example request
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the Reserve Bank of Australia?"}'
```

### Example response
```json
{
  "question": "What is the Reserve Bank of Australia?",
  "final_answer": "The Reserve Bank of Australia (RBA) is Australia central bank and banknote issuing authority, established on 14 January 1960.",
  "analyst_facts": "• RBA established 14 January 1960\n• Central bank and banknote authority\n• Net worth A$101 billion",
  "success": true,
  "time_sec": 7.23,
  "pipeline": "retriever → analyst → synthesiser"
}
```

---

## Project Structure

```
Multi-Agent-RAG-System-for-Enterprise-Document-Intelligence/
├── agents/
│   ├── retriever.py        # Retriever Agent — FAISS vector search
│   ├── analyst.py          # Analyst Agent — fact extraction
│   └── synthesiser.py      # Synthesiser Agent — answer generation
├── tools/
│   ├── retrieval_tool.py   # MCP-style vector search tool
│   ├── calculator_tool.py  # MCP-style calculator tool
│   └── summarise_tool.py   # MCP-style summarisation tool
├── src/
│   ├── graph.py            # LangGraph orchestration
│   ├── api.py              # FastAPI REST wrapper
│   ├── config.py           # configuration
│   ├── data_loader.py      # MS MARCO dataset loading
│   └── evaluate.py         # evaluation framework
├── notebooks/
│   ├── 01_data_and_setup.ipynb
│   ├── 02_agents_and_graph.ipynb
│   ├── 03_evaluation_and_plots.ipynb
│   └── 04_fastapi_and_docker.ipynb
├── results/
│   ├── evaluation_results.csv
│   ├── eval_summary.json
│   └── figures/
│       ├── evaluation_results.png
│       └── agent_contribution.png
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup & Reproducibility

### 1. Clone and install

```bash
git clone https://github.com/chaitanyamhetre/Multi-Agent-RAG-System-for-Enterprise-Document-Intelligence.git
cd Multi-Agent-RAG-System-for-Enterprise-Document-Intelligence
pip install -r requirements.txt
```

### 2. Configure API key

```bash
export GROQ_API_KEY=your_groq_key_here
```

Free API key: console.groq.com

### 3. Generate data

```bash
python src/data_loader.py
```

### 4. Run the agent

```bash
python src/graph.py
```

### 5. Start the API

```bash
uvicorn src.api:app --reload
```

### 6. Run with Docker

```bash
docker-compose up --build
```

### 7. Run on Google Colab

All notebooks run on Google Colab free tier. Open notebooks in order:
01 → 02 → 03 → 04

---

## Limitations & Future Work

**Evaluation metric:** Keyword matching underestimates answer quality.
LLMs paraphrase correctly but ground truth keywords may not appear
verbatim. Future work: BERTScore or human evaluation.

**Sequential pipeline:** Agents run in fixed sequence. Future work:
conditional routing — orchestrator decides which agents to invoke
based on question type.

**Tool set:** Currently 3 tools. Natural extensions: web search tool,
SQL query tool, code execution tool.

**Scale:** 500-document corpus. Production deployment would use a
larger domain-specific index with periodic refresh.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.3-green)
![LangGraph](https://img.shields.io/badge/LangGraph-1.2-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688)
![Docker](https://img.shields.io/badge/Docker-containerised-2496ED)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.1-purple)
![FAISS](https://img.shields.io/badge/FAISS-VectorSearch-red)

- **Orchestration:** LangGraph StateGraph
- **Agents:** 3 specialised agents — Retriever, Analyst, Synthesiser
- **LLM:** Llama 3.1 8B Instruct via Groq free API
- **Vector search:** FAISS + sentence-transformers (all-MiniLM-L6-v2)
- **API:** FastAPI + Uvicorn
- **Containerisation:** Docker + docker-compose
- **Dataset:** MS MARCO v1.1 via HuggingFace

---
