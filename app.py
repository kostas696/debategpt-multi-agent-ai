# app.py

import os
from dotenv import load_dotenv
from langsmith import traceable

from state.debate_state import DebateState
from graph.debate_graph import build_debate_graph

# Fallback for transcript printing if utils module not ready
try:
    from utils.debate_visualizer import print_debate_transcript
except ImportError:
    def print_debate_transcript(state: DebateState):
        print("\n[Fallback] Printing raw transcript:\n")
        for msg in state.history:
            speaker = "Human" if msg.type == "human" else "AI"
            print(f"\n{speaker}: {msg.content.strip()}")

# Load environment variables
load_dotenv()


@traceable(name="DebateGPT - Main")
def main():
    topic = os.getenv("DEBATE_TOPIC", "AI will replace most jobs")

    initial_state = DebateState(
        topic=topic,
        history=[],
        turn_count=0,
        last_speaker=None,
        verdict=None
    )

    print(f"\nStarting Debate on: {topic}")
    print("=" * 60)

    try:
        # Build LangGraph
        app = build_debate_graph()

        # Run LangGraph and get dict result
        result = app.invoke(initial_state)

        # LangGraph returns dict — extract DebateState
        final_state = result["state"] if isinstance(result, dict) and "state" in result else result

        print("\nDebate Complete!")
        print("=" * 60)

        if final_state.verdict:
            print("\nFinal Verdict:\n")
            print(final_state.verdict)
        else:
            print("\nNo verdict was reached.\n")

        print("\nFull Transcript:\n")
        print_debate_transcript(final_state)

    except KeyboardInterrupt:
        print("\nDebate interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")


if __name__ == "__main__":
    main()