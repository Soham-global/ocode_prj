from fastapi import APIRouter

from app.schemas import (
    QueryRequest,
    SuccessResponse,
    RejectedResponse,
    AnswerPayload,
    ScopeResponse,
    HealthResponse,
)
from app.graph.agent_graph import run_agent
from app.guardrails.scope_config import ALLOWED_SCOPE

router = APIRouter()


@router.post("/agent/query", response_model=None)
def agent_query(request: QueryRequest):
    final_state = run_agent(request.query)

    if final_state.get("is_in_scope"):
        return SuccessResponse(
            response=AnswerPayload(answer=final_state["answer"])
        )

    reason = final_state.get("rejection_reason") or "Request is outside the agent's allowed scope"
    return RejectedResponse(reason=reason)


@router.get("/agent/scope", response_model=ScopeResponse)
def agent_scope():
    return ScopeResponse(
        allowed_topics=ALLOWED_SCOPE["topics"],
        response_style=ALLOWED_SCOPE["response_style"],
    )


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse()
