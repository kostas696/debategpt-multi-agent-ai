from langgraph.graph import StateGraph, END
from state.debate_state import DebateState
from agents.proponent import proponent_node
from agents.opponent import opponent_node
from agents.moderator import moderator_node, should_continue

from langchain_core.runnables import RunnableLambda

def build_debate_graph():
    graph = StateGraph(DebateState)

    # Add agent nodes
    graph.add_node("proponent", proponent_node)
    graph.add_node("opponent", opponent_node)
    graph.add_node("moderator", moderator_node)

    # Entry point
    graph.set_entry_point("proponent")

    # Static edges
    graph.add_edge("proponent", "opponent")
    graph.add_edge("opponent", "moderator")

    # Conditional branching using RunnableLambda
    graph.add_conditional_edges(
        "moderator",
        RunnableLambda(should_continue),
        {
            "continue": "proponent",
            "end": END
        }
    )

    return graph.compile()
