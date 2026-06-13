from typing import TypedDict, Optional

from app.guardrails.scope_checker import check_scope, ScopeDecision
from app.config import settings


class AgentState(TypedDict):
    query: str
    is_in_scope: bool
    rejection_reason: Optional[str]
    answer: Optional[str]


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


def agent_node(state: AgentState) -> AgentState:
    query = state["query"]

    if settings.LLM_PROVIDER == "groq":
        answer = _call_groq(query)
    else:
        answer = (
            "This is a high-level explanation related to web scraping. "
            f"Topic discussed: '{query}'. "
            "(Mock response — set LLM_PROVIDER=groq and GROQ_API_KEY "
            "to get real LLM-generated answers.)"
        )

    state["answer"] = answer
    return state


def _call_groq(query: str) -> str:
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
