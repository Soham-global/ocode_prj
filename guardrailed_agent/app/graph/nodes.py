"""
LangGraph node functions for the Guardrailed AI Agent.

Two nodes:
1. guardrail_node  -> programmatically validates the query's scope.
   If out-of-scope/blocked/ambiguous, sets a rejection and the graph
   terminates early (handled in agent_graph.py via conditional edges).
2. agent_node      -> only reached if the query passed the guardrail.
   Calls the LLM (Groq/Llama) to produce a high-level, explanatory
   answer restricted to the allowed scope.
"""

from typing import TypedDict, Optional

from app.guardrails.scope_checker import check_scope, ScopeDecision
from app.config import settings


# -------------------------------------------------------------------
# Graph state definition
# -------------------------------------------------------------------
class AgentState(TypedDict):
    query: str
    is_in_scope: bool
    rejection_reason: Optional[str]
    answer: Optional[str]


# -------------------------------------------------------------------
# System prompt restricting the LLM to the allowed scope
# (Defense-in-depth: prompt-level restriction ON TOP OF the
# programmatic guardrail, not instead of it.)
# -------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a specialized assistant that ONLY discusses web scraping "
    "concepts, JavaScript-rendered websites, headless browsers, "
    "CAPTCHA detection and high-level (non-bypass) handling strategies, "
    "and the ethical/legal considerations of web scraping. "
    "Always respond in a high-level, explanatory manner. "
    "Never provide instructions for illegal CAPTCHA bypass, scraping "
    "without permission, or any unethical activity. "
    "Keep answers concise and informative."
)


# -------------------------------------------------------------------
# Node 1: Guardrail check (programmatic, deterministic)
# -------------------------------------------------------------------
def guardrail_node(state: AgentState) -> AgentState:
    query = state.get("query", "")
    decision, reason = check_scope(query)

    if decision == ScopeDecision.IN_SCOPE:
        state["is_in_scope"] = True
        state["rejection_reason"] = None
    else:
        state["is_in_scope"] = False
        state["rejection_reason"] = reason

    return state


# -------------------------------------------------------------------
# Node 2: Agent response (only reached for in-scope queries)
# -------------------------------------------------------------------
def agent_node(state: AgentState) -> AgentState:
    query = state["query"]

    if settings.LLM_PROVIDER == "groq":
        answer = _call_groq(query)
    else:
        # Mock provider: deterministic canned response, no API key needed.
        answer = (
            "This is a high-level explanation related to web scraping. "
            f"Topic discussed: '{query}'. "
            "(Mock response — set LLM_PROVIDER=groq and GROQ_API_KEY "
            "to get real LLM-generated answers.)"
        )

    state["answer"] = answer
    return state


def _call_groq(query: str) -> str:
    """Call Groq's Llama model via langchain-groq."""
    from langchain_groq import ChatGroq
    from langchain_core.messages import SystemMessage, HumanMessage

    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.3,
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]

    result = llm.invoke(messages)
    return result.content