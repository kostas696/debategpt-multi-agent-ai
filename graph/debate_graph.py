# graph/debate_graph.py

from langgraph.graph import StateGraph, END
from state.debate_state import DebateState
from agents.proponent import proponent_node
from agents.opponent import opponent_node
from agents.moderator import moderator_node, should_continue

# Build LangGraph StateGraph
def build_debate_graph():
    graph = StateGraph(DebateState)

    # Register agent nodes
    graph.add_node("proponent", proponent_node)
    graph.add_node("opponent", opponent_node)
    graph.add_node("moderator", moderator_node)

    # Set entry point
    graph.set_entry_point("proponent")

    # Define flow
    graph.add_edge("proponent", "opponent")
    graph.add_edge("opponent", "moderator")

    # Conditional branching: end or loop
    graph.add_conditional_edges(
        "moderator",
        condition=should_continue,
        path_map={
            "continue": "proponent",
            "end": END
        }
    )

    return graph.compile()
