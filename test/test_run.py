# test/test_run.py

import pytest
from graph.debate_graph import build_debate_graph

def test_debate_flow():
    app = build_debate_graph()

    initial_state = {
        "topic": "Should space exploration be privatized?",
        "history": [],
        "turn_count": 0,
        "last_speaker": "",
        "verdict": None
    }

    final_state = app.invoke(initial_state)

    # Basic assertions
    assert final_state["verdict"] is not None, "Debate did not produce a verdict."
    assert isinstance(final_state["history"], list), "History is not a list."
    assert len(final_state["history"]) > 0, "Debate history is empty."
    assert final_state["turn_count"] > 0, "Debate did not progress."

    print("Debate flow test passed.")
