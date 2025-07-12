# streamlit_app.py

import os
import streamlit as st
from dotenv import load_dotenv
from graph.debate_graph import build_debate_graph

load_dotenv()

st.set_page_config(page_title="DebateGPT", layout="centered")

st.title("DebateGPT: Multi-Agent AI Debate Simulator")
st.markdown("Simulate a structured AI-powered debate between two agents with a neutral moderator.")

# Input
topic = st.text_input("Enter a debate topic:", value="AI will replace most jobs")

run_button = st.button("Start Debate")

if run_button:
    with st.spinner("Running debate... please wait"):
        app = build_debate_graph()

        initial_state = {
            "topic": topic,
            "history": [],
            "turn_count": 0,
            "last_speaker": "",
            "verdict": None
        }

        final_state = app.invoke(initial_state)

    st.success("Debate Complete!")

    st.subheader("Final Verdict")
    st.markdown(final_state.get("verdict", "*No verdict available.*"))

    st.subheader("Debate Transcript")
    for msg in final_state["history"]:
        if msg.type == "human":
            st.markdown(f"**Human:** {msg.content}")
        elif msg.type == "ai":
            st.markdown(f"**AI:** {msg.content}")
