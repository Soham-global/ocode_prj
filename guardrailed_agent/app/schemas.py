from typing import Literal, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's natural language query")


class AnswerPayload(BaseModel):
    answer: str


class SuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    response: AnswerPayload


class RejectedResponse(BaseModel):
    status: Literal["rejected"] = "rejected"
    reason: str


class ScopeResponse(BaseModel):
    allowed_topics: list[str]
    response_style: str


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "guardrailed-agent"
