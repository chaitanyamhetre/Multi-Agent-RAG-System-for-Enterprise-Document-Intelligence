# tools/retrieval_tool.py
"""
Vector retrieval tool — MCP-style tool interface.
Used by the Retriever Agent to search the document corpus.
"""
import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langchain.tools import tool

EMBEDDINGS_PATH = "data/processed/embeddings.npy"

df_docs  = pd.read_csv("data/processed/documents.csv")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

if os.path.exists(EMBEDDINGS_PATH):
    embeddings = np.load(EMBEDDINGS_PATH)
else:
    texts      = df_docs["text"].tolist()
    embeddings = embedder.encode(texts, show_progress_bar=True, batch_size=64)
    embeddings = np.array(embeddings).astype("float32")
    np.save(EMBEDDINGS_PATH, embeddings)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.astype("float32"))
print(f"Retrieval tool: index built with {index.ntotal} vectors")


@tool
def search_documents(query: str) -> str:
    """
    Search the document knowledge base for passages relevant to the query.
    Use this tool to find factual information from the document corpus.
    Input: natural language search query
    Output: top 3 relevant document passages
    """
    q_emb              = embedder.encode([query]).astype("float32")
    distances, indices = index.search(q_emb, 3)

    results = []
    for rank, idx in enumerate(indices[0]):
        text = df_docs.iloc[idx]["text"]
        results.append(f"[Document {rank+1}]\n{text[:500]}")

    return "\n\n".join(results)
