# src/test_api.py
"""
Tests the FastAPI endpoints.
Run AFTER starting server: uvicorn src.api:app --reload
"""
import requests, json

BASE_URL = "http://localhost:8000"

def test_root():
    print("=== ROOT ===")
    r = requests.get(f"{BASE_URL}/")
    print(json.dumps(r.json(), indent=2))

def test_health():
    print("\n=== HEALTH ===")
    r = requests.get(f"{BASE_URL}/health")
    print(json.dumps(r.json(), indent=2))

def test_ask(question: str):
    print(f"\n=== ASK ===")
    print(f"Q: {question}")
    r = requests.post(
        f"{BASE_URL}/ask",
        json={"question": question}
    )
    data = r.json()
    print(f"Status:  {r.status_code}")
    print(f"Answer:  {data.get('final_answer', '')[:200]}")
    print(f"Success: {data.get('success')}")
    print(f"Time:    {data.get('time_sec')}s")

if __name__ == "__main__":
    test_root()
    test_health()
    test_ask("What is the Reserve Bank of Australia?")
    test_ask("What is risk-based authentication?")
