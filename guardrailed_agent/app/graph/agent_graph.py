from langgraph.graph import StateGraph, END

from app.graph.nodes import AgentState, guardrail_node, agent_node


def _route_after_guardrail(state: AgentState) -> str:
    return "agent" if state.get("is_in_scope") else "end"


_graph = StateGraph(AgentState)
_graph.add_node("guardrail", guardrail_node)
_graph.add_node("agent", agent_node)
_graph.set_entry_point("guardrail")
_graph.add_conditional_edges("guardrail", _route_after_guardrail, {"agent": "agent", "end": END})
_graph.add_edge("agent", END)

compiled_agent_graph = _graph.compile()


def run_agent(query: str) -> AgentState:
    initial_state: AgentState = {
        "query": query,
        "is_in_scope": False,
        "rejection_reason": None,
        "answer": None,
    }
    return compiled_agent_graph.invoke(initial_state)
