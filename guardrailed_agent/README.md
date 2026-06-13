# Guardrailed AI Agent

A scope-restricted AI agent built with LangChain and LangGraph. It only answers questions about web scraping topics. Everything else is rejected before it ever reaches the LLM.

---

## Allowed Scope

The agent only responds to queries about:

1. Web scraping concepts
2. JavaScript-rendered websites
3. CAPTCHA detection and high-level handling strategies (no illegal bypass)
4. Headless browsers used for scraping
5. Ethical and legal considerations of web scraping

All answers are high-level and explanatory. Anything outside this list is rejected.

---

## Guardrail Enforcement Strategy

Guardrails run as a node inside the LangGraph execution flow — not as a prompt instruction:

```
START → guardrail_node → (conditional edge)
                            ├─ in scope   → agent_node → END
                            └─ out of scope / blocked / ambiguous → END
```

The `guardrail_node` runs a deterministic keyword check on every incoming query:

1. If the query contains any blocked keyword (illegal bypass, personal/medical/political topics, greetings, etc.) → rejected immediately, highest priority.
2. If the query contains at least one allowed keyword (scraping, headless, captcha, etc.) → passes to the agent.
3. If the query is empty, too short, or matches nothing → rejected as ambiguous.

Out-of-scope queries terminate at `END` right after the guardrail node and never reach `agent_node`.

Rejection response format:
```json
{ "status": "rejected", "reason": "Topic not allowed by agent guardrails" }
```

---

## API Endpoints

### `POST /agent/query`
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
Returns the agent's enforced allowed topics and response style.

### `GET /health`
```json
{ "status": "ok", "service": "guardrailed-agent" }
```

All responses including errors are JSON only.

---

## Running with Docker

### Prerequisites
- Docker and Docker Compose installed
- A Groq API key from [console.groq.com](https://console.groq.com)

### Setup

```bash
cp .env.example .env
# edit .env and set your GROQ_API_KEY
```

```bash
docker-compose up --build
```

API available at `http://localhost:8000`.

> Set `LLM_PROVIDER=mock` in `.env` to run without a real API key — useful for testing guardrail logic only.

---

## Testing the API

### Health check
```bash
curl http://localhost:8000/health
```

### Get scope
```bash
curl http://localhost:8000/agent/scope
```

### In-scope query (accepted)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do headless browsers help scrape JS-heavy websites?"}'
```

### Out-of-scope query (rejected)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```

### Ambiguous query (rejected)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "hi"}'
```

### Illegal CAPTCHA bypass (blocked)
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How can I bypass captcha to scrape illegally?"}'
```

### Automated tests (inside container)
```bash
docker-compose exec agent sh -c "pip install pytest httpx && pytest"
```

---

## Project Structure

```
guardrailed_agent/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── graph/
│   │   ├── agent_graph.py
│   │   └── nodes.py
│   ├── guardrails/
│   │   ├── scope_checker.py
│   │   └── scope_config.py
│   └── api/
│       └── routes.py
├── tests/
│   └── test_api.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```
