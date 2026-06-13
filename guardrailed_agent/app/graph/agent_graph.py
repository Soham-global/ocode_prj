from langgraph.graph import StateGraph, END

from app.graph.nodes import AgentState, guardrail_node, agent_node


def _route_after_guardrail(state: AgentState) -> str:
    if state.get("is_in_scope"):
        return "agent"
    return "end"


def build_agent_graph():
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


compiled_agent_graph = build_agent_graph()


def run_agent(query: str) -> AgentState:
    initial_state: AgentState = {
        "query": query,
        "is_in_scope": False,
        "rejection_reason": None,
        "answer": None,
    }
    final_state = compiled_agent_graph.invoke(initial_state)
    return final_state
