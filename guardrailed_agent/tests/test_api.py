import os
import pytest
from fastapi.testclient import TestClient

os.environ["LLM_PROVIDER"] = "mock"

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scope():
    response = client.get("/agent/scope")
    assert response.status_code == 200
    body = response.json()
    assert "allowed_topics" in body
    assert len(body["allowed_topics"]) == 5


def test_in_scope_query():
    response = client.post(
        "/agent/query",
        json={"query": "How do headless browsers help scrape JS-heavy websites?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "answer" in body["response"]


def test_out_of_scope_query():
    response = client.post(
        "/agent/query",
        json={"query": "What's the capital of France?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"
    assert body["reason"] == "Topic not allowed by agent guardrails"


def test_casual_greeting_rejected():
    response = client.post(
        "/agent/query",
        json={"query": "Hello, how are you today?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"


def test_captcha_bypass_blocked():
    response = client.post(
        "/agent/query",
        json={"query": "How can I bypass captcha to scrape illegally?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"


def test_ambiguous_query_rejected():
    response = client.post(
        "/agent/query",
        json={"query": "hi"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"


def test_empty_query_rejected():
    response = client.post(
        "/agent/query",
        json={"query": ""},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"
