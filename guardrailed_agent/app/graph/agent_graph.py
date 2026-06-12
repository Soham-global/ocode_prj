"""
LangGraph graph definition for the Guardrailed AI Agent.

Flow:
    START -> guardrail_node -> (conditional)
                                  - in scope   -> agent_node -> END
                                  - out of scope/blocked/ambiguous -> END

The guardrail check happens FIRST and is enforced as part of the graph's
execution flow (not just a pre-check in the API layer), satisfying the
requirement that out-of-scope requests terminate execution early and
never reach the agent's response logic.
"""

from langgraph.graph import StateGraph, END

from app.graph.nodes import AgentState, guardrail_node, agent_node


def _route_after_guardrail(state: AgentState) -> str:
    """Conditional edge: decide whether to proceed to the agent node."""
    if state.get("is_in_scope"):
        return "agent"
    return "end"


def build_agent_graph():
    """Construct and compile the LangGraph for the agent."""
    graph = StateGraph(AgentState)

    graph.add_node("guardrail", guardrail_node)
    graph.add_node("agent", agent_node)

    graph.set_entry_point("guardrail")

    graph.add_conditional_edges(
        "guardrail",
        _route_after_guardrail,
        {
            "agent": "agent",
            "end": END,
        },
    )

    graph.add_edge("agent", END)

    return graph.compile()


# Compile once at import time; reused across requests.
compiled_agent_graph = build_agent_graph()


def run_agent(query: str) -> AgentState:
    """
    Execute the graph for a given query and return the final state.

    The caller (API layer) inspects `is_in_scope` to decide whether to
    return a success or rejected response.
    """
    initial_state: AgentState = {
        "query": query,
        "is_in_scope": False,
        "rejection_reason": None,
        "answer": None,
    }
    final_state = compiled_agent_graph.invoke(initial_state)
    return final_state