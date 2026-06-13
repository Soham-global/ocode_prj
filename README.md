# Guardrailed AI Agent (LangChain + LangGraph)

A scope-restricted AI agent that answers questions **only** about web
scraping topics, with programmatic guardrails enforced inside a
LangGraph execution flow. Out-of-scope, ambiguous, or unethical/illegal
requests are rejected with a deterministic JSON response and never
reach the LLM.

---

## 1. Allowed Scope

The agent only answers questions about:

1. Web scraping concepts
2. JavaScript-rendered websites
3. CAPTCHA detection and high-level handling strategies (no illegal bypass)
4. Headless browsers used for scraping
5. Ethical and legal considerations of web scraping

All responses are high-level and explanatory.

Everything else — general programming, casual conversation, personal/
medical/legal/political questions, or requests for illegal scraping /
CAPTCHA bypass — is rejected.

Retrieve this scope programmatically via `GET /agent/scope`.

---

## 2. Guardrail Enforcement Strategy

Guardrails are enforced **programmatically**, as a node in the LangGraph
flow — not just via prompting:

```
START -> guardrail_node -> (conditional edge)
                              ├─ in scope        -> agent_node -> END
                              └─ out of scope /
                                 blocked /
                                 ambiguous        -> END (rejected)
```

- **`guardrail_node`** (`app/guardrails/scope_checker.py`) runs a
  deterministic, rule-based check against the query:
  1. **Blocked keywords** (illegal CAPTCHA bypass, unrelated personal/
     medical/legal/political topics, casual greetings, general
     programming, etc.) → immediate rejection, highest priority.
  2. **Allowed keywords** (scraping, headless browsers, CAPTCHA,
     JS-rendering, ethics/legal, etc.) → at least one match required
     to proceed.
  3. **Fail-closed**: empty, too-short, or keyword-less queries are
     treated as ambiguous and rejected by default.

- Only if the query is classified `in_scope` does the graph route to
  **`agent_node`**, which calls the LLM (Groq/Llama) with a system
  prompt that reinforces the same restrictions as defense-in-depth.

- Out-of-scope requests terminate at `END` immediately after the
  guardrail node — they never reach `agent_node`.

### Rejection response format

```json
{ "status": "rejected", "reason": "Topic not allowed by agent guardrails" }
```

---

## 3. API Endpoints

### `POST /agent/query`

Request:
```json
{ "query": "How do headless browsers help scrape JS-heavy websites?" }
```

In-scope response:
```json
{ "status": "success", "response": { "answer": "..." } }
```

Out-of-scope response:
```json
{ "status": "rejected", "reason": "Topic not allowed by agent guardrails" }
```

### `GET /agent/scope`

Returns the enforced scope (allowed topics + response style).

### `GET /health`

```json
{ "status": "ok", "service": "guardrailed-agent" }
```

All responses — including validation/server errors — are JSON only.

---

## 4. Running with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Setup

1. Copy the example env file and add your key:
   ```bash
   cp .env.example .env
   # edit .env and set GROQ_API_KEY=your_actual_key
   ```

2. Build and run:
   ```bash
   docker-compose up --build
   ```

3. The API is now available at `http://localhost:8000`.

> If `LLM_PROVIDER=mock` (or no API key is set), the agent returns a
> deterministic mock answer for in-scope queries — useful for testing
> the guardrail logic without any external API calls.

---

## 5. Testing the API

### Health check
```bash
curl http://localhost:8000/health
```

### Scope
```bash
curl http://localhost:8000/agent/scope
```

### In-scope query (accepted)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do headless browsers help scrape JS-heavy websites?"}'
```
Expected: `{"status": "success", "response": {"answer": "..."}}`

### Out-of-scope query (rejected)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```
Expected: `{"status": "rejected", "reason": "Topic not allowed by agent guardrails"}`

### Ambiguous query (rejected)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "hi"}'
```
Expected: `{"status": "rejected", "reason": "..."}`

### Illegal CAPTCHA bypass request (blocked)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How can I bypass captcha to scrape illegally?"}'
```
Expected: `{"status": "rejected", "reason": "..."}`

### Automated tests

Inside the running container:
```bash
docker-compose exec agent uv run pytest
```

---

## 6. Project Structure

```
guardrailed_agent/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── config.py            # Settings (LLM provider, Groq config)
│   ├── schemas.py            # Pydantic request/response models
│   ├── graph/
│   │   ├── agent_graph.py    # LangGraph definition + routing
│   │   └── nodes.py          # guardrail_node, agent_node
│   ├── guardrails/
│   │   ├── scope_checker.py  # Programmatic scope validation
│   │   └── scope_config.py   # Allowed/blocked topic keywords
│   └── api/
│       └── routes.py         # /agent/query, /agent/scope, /health
├── tests/
│   └── test_api.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```