"""
Programmatic guardrail enforcement for the Guardrailed AI Agent.

This module performs scope validation BEFORE any query reaches the
LLM/agent logic. It is deterministic and rule-based (not prompt-based),
satisfying the requirement that guardrails be enforced programmatically.

Fail-closed policy:
- If a query contains any BLOCKED_KEYWORDS -> reject (BLOCKED).
- If a query is empty/too short/too vague -> reject (AMBIGUOUS).
- If a query does not contain at least one ALLOWED_KEYWORDS match -> reject (OUT_OF_SCOPE).
- Only if it passes all checks is it considered IN-SCOPE.
"""

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


# Minimum normalized length of a query for it to be considered non-ambiguous.
MIN_QUERY_LENGTH = 4


def _normalize(text: str) -> str:
    return text.strip().lower()


def check_scope(query: str) -> tuple[ScopeDecision, str | None]:
    """
    Validate a user query against the agent's allowed scope.

    Returns:
        (decision, rejection_reason)
        - decision is one of ScopeDecision
        - rejection_reason is None if decision == IN_SCOPE,
          otherwise a human-readable string explaining the rejection.
    """
    if query is None:
        return ScopeDecision.AMBIGUOUS, REJECTION_REASON_AMBIGUOUS

    normalized = _normalize(query)

    # Fail closed: empty or too-short queries are ambiguous -> reject
    if len(normalized) < MIN_QUERY_LENGTH:
        return ScopeDecision.AMBIGUOUS, REJECTION_REASON_AMBIGUOUS

    # 1. Check for explicitly blocked content first (highest priority).
    for blocked in BLOCKED_KEYWORDS:
        if blocked in normalized:
            return ScopeDecision.BLOCKED, REJECTION_REASON_BLOCKED

    # 2. Check for at least one allowed-topic keyword.
    for allowed in ALLOWED_KEYWORDS:
        if allowed in normalized:
            return ScopeDecision.IN_SCOPE, None

    # 3. Fail closed: no allowed keyword matched -> out of scope.
    return ScopeDecision.OUT_OF_SCOPE, REJECTION_REASON_OUT_OF_SCOPE


def is_in_scope(query: str) -> bool:
    """Convenience boolean wrapper around check_scope."""
    decision, _ = check_scope(query)
    return decision == ScopeDecision.IN_SCOPE