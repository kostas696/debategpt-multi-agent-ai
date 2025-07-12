# app.py

import os
from dotenv import load_dotenv
from graph.debate_graph import build_debate_graph
from langsmith import traceable

load_dotenv()

@traceable(name="DebateGPT - Main")
def main():
    topic = os.getenv("DEBATE_TOPIC", "AI will replace most jobs")

    initial_state = {
        "topic": topic,
        "history": [],
        "turn_count": 0,
        "last_speaker": "",
        "verdict": None
    }

    print(f"Starting Debate on: {topic}")
    print("=" * 60)

    app = build_debate_graph()

    final_state = app.invoke(initial_state)

    print("\nDebate Complete!")
    print("=" * 60)
    print("\nFinal Verdict:\n")
    print(final_state.get("verdict", "No verdict reached."))

    print("\nFull Transcript:")
    for msg in final_state["history"]:
        speaker = "Human" if msg.type == "human" else "AI"
        print(f"\n{speaker}: {msg.content.strip()}")

if __name__ == "__main__":
    main()