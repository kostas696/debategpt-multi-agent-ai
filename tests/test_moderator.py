# tests/test_moderator.py

from langchain_core.messages import HumanMessage, AIMessage
from state.debate_state import DebateState
from agents.moderator import moderator_node, should_continue

def test_moderator_node():
    print("Running Moderator Node test...")

    # Simulate prior AI responses (opponent then proponent)
    history = [
        HumanMessage(content="Debate topic: Should AI replace teachers?"),
        AIMessage(content="AI cannot replace teachers due to the emotional and human aspects of education."),
        AIMessage(content="AI can enhance education and provide personalized learning, making it a strong candidate to assist or even replace teachers."),
    ]

    state = DebateState(
        topic="Should AI replace teachers?",
        history=history,
        turn_count=1,
        last_speaker="opponent"
    )

    updated_state = moderator_node(state)

    print("\n--- MODERATOR OUTPUT ---")
    for msg in updated_state.history[-2:]:
        print(f"{msg.__class__.__name__}: {msg.content}")

    if updated_state.verdict:
        print("\n--- VERDICT ---")
        print(updated_state.verdict)

    assert isinstance(updated_state.history[-1], AIMessage), "Last message should be from moderator"
    assert updated_state.error is None, f"Moderator threw an error: {updated_state.error}"

    print("Moderator Node test passed.")

if __name__ == "__main__":
    test_moderator_node()
