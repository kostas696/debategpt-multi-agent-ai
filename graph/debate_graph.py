from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# Debate state and agents
from state.debate_state import DebateState
from agents.proponent import proponent_node
from agents.opponent import opponent_node
from agents.moderator import moderator_node, should_continue

import os


def build_debate_graph():
    # Initialize LangGraph with typed state
    graph = StateGraph(DebateState)

    # --- Agent Nodes ---
    graph.add_node("proponent", proponent_node)
    graph.add_node("opponent", opponent_node)
    graph.add_node("moderator", moderator_node)

    # --- Edges (debate flow) ---
    graph.set_entry_point("proponent")
    graph.add_edge("proponent", "opponent")
    graph.add_edge("opponent", "moderator")

    # --- Conditional Branching ---
    graph.add_conditional_edges(
        "moderator",
        RunnableLambda(should_continue),
        {
            "continue": "proponent",
            "end": END
        }
    )

    # --- Compile and Visualize ---
    compiled_graph = graph.compile()

    # Ensure the assets folder exists
    os.makedirs("assets", exist_ok=True)
    try:
        compiled_graph.get_graph().draw_png("assets/debate_graph.png")
        print("[✓] Graph image saved to assets/debate_graph.png")
    except Exception as e:
        print(f"[Warning] Could not render graph image: {e}")

    return compiled_graph