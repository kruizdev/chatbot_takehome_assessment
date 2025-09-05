# Chatbot Take‑Home (Python + FastAPI + pytest)

Implement features in an existing chatbot service and make the tests pass.
Timebox: ~6–8 focused hours (hard-but-fair).

## What you’ll build
1) **Hybrid Retrieval (RAG‑lite)**: BM25 + dense embeddings → combined score by α.  
2) **Short‑term Memory**: size-capped, role-aware truncation; durable backend using SQLite (kv).  
3) **Tool Use**: airline pet policies tool (schema-validated); route must call tool and merge result.  
4) **Safety**: redact PII in logs; basic denylist gate.  
5) **Rate Limiting**: token bucket per user_id.  
6) **Telemetry**: emit simple spans/events, return a `trace-id` header.  
7) **/chat** API: accepts a thread, streams assistant text; tools are invisible mid-stream; citations in trailer.

> No external network calls in tests. Embeddings/LLM are mocked; your code must be structured to accept mocks.

## Getting started
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q OR python -m pytest -q 
# You'll see some failing tests (by design).
uvicorn app.main:app --reload
# Will not work initially, by design. Go to http://127.0.0.1:8000/docs to check if it's working
```

### Run a quick smoke
```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d @tests/fixtures/minimal.json
```

## Repo layout
```
.
├─ app/
│  ├─ main.py              # FastAPI app
│  ├─ routes/chat.py       # POST /chat  (streaming; tool loop)
│  ├─ llm/
│  │  ├─ base.py
│  │  └─ mock.py
│  ├─ retrieval/
│  │  ├─ bm25.py           # baseline
│  │  └─ retriever.py      # TODO: hybrid w/ α
│  ├─ memory/
│  │  ├─ base.py
│  │  ├─ inmem.py
│  │  └─ kv.py             # TODO: SQLite-backed
│  ├─ tools/
│  │  ├─ airline_pets.py
│  │  └─ registry.py
│  ├─ safety/guard.py      # TODO: redact + denylist
│  ├─ rate/limiter.py      # TODO: token bucket
│  ├─ telemetry/trace.py
│  └─ schemas/message.py
├─ data/
│  ├─ airline_policies.jsonl
│  └─ docs/*.md
├─ tests/
│  ├─ unit/*.py
│  ├─ integration/*.py
│  └─ fixtures/*
├─ requirements.txt
├─ pyproject.toml
└─ .github/workflows/ci.yml
```

## What we test
- `tests/unit/retrieval_test.py`: NDCG@5 improvement over BM25 on a tiny set (**fails until you implement hybrid**).
- `tests/unit/memory_test.py`: truncation + durability (**kv backend must pass**).
- `tests/unit/tools_test.py`: tool call schema + basic Q/A from corpus.
- `tests/unit/safety_test.py`: PII redaction + denylist (**fails**).
- `tests/unit/rate_test.py`: token bucket behavior (**fails**).
- `tests/integration/chat_end2end_test.py`: end‑to‑end flow via FastAPI (currently xfail with TODOs).
- `tests/integration/streaming_test.py`: streaming contract (xfail).

## Deliverables
1. **Working code that passes all visible tests**
   - `pytest` must be green.

2. **Answers to 4 short design prompts in `README.md`**
   - (a) How you chose **α (hybrid weight)** and tradeoffs  
   - (b) Memory truncation policy rationale  
   - (c) Safety false-positive/negative considerations  
   - (d) What you’d productionize next and why  

3. **A 5–8 minute walkthrough**
   - File changes  
   - How to run locally  
   - How you debugged one failing test  

---

## Scoring Rubric (100 pts)

### Correctness — 40 pts
- Retrieval gains vs baseline (15)  
- Memory correctness (10)  
- Tool call flow (10)  
- Rate limit (5)  

### Reliability & Safety — 20 pts
- Redaction coverage (10)  
- No PII in logs (5)  
- Graceful errors (5)  

### Code Quality — 20 pts
- Typed functions and clear structure  
- Small, focused functions  
- Comments where needed  
- Clear and descriptive test names  

### Performance — 10 pts
- Retriever latency within thresholds  
- Memory operations within thresholds  

### Design Reasoning — 10 pts
- Clear tradeoffs explained in README answers  
