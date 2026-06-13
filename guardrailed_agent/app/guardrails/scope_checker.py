from enum import Enum

from app.guardrails.scope_config import (
    ALLOWED_KEYWORDS,
    BLOCKED_KEYWORDS,
    REJECTION_REASON_OUT_OF_SCOPE,
    REJECTION_REASON_AMBIGUOUS,
    REJECTION_REASON_BLOCKED,
)


class ScopeDecision(str, Enum):
    IN_SCOPE = "in_scope"
    OUT_OF_SCOPE = "out_of_scope"
    AMBIGUOUS = "ambiguous"
    BLOCKED = "blocked"


MIN_QUERY_LENGTH = 4


def _normalize(text: str) -> str:
    return text.strip().lower()


def check_scope(query: str) -> tuple[ScopeDecision, str | None]:
    if query is None:
        return ScopeDecision.AMBIGUOUS, REJECTION_REASON_AMBIGUOUS

    normalized = _normalize(query)

    if len(normalized) < MIN_QUERY_LENGTH:
        return ScopeDecision.AMBIGUOUS, REJECTION_REASON_AMBIGUOUS

    for blocked in BLOCKED_KEYWORDS:
        if blocked in normalized:
            return ScopeDecision.BLOCKED, REJECTION_REASON_BLOCKED

    for allowed in ALLOWED_KEYWORDS:
        if allowed in normalized:
            return ScopeDecision.IN_SCOPE, None

    return ScopeDecision.OUT_OF_SCOPE, REJECTION_REASON_OUT_OF_SCOPE


def is_in_scope(query: str) -> bool:
    decision, _ = check_scope(query)
    return decision == ScopeDecision.IN_SCOPE
