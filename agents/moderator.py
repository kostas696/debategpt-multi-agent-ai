import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from huggingface_hub.inference._client import InferenceClient
from tools.persona_prompt_tool import get_persona_prompt
from tools.fallacy_detector import detect_fallacies

MAX_TURNS = 4  # Total debate rounds before verdict

llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id=os.getenv("LLM_MODEL", "google/flan-t5-base"),
        task="text-generation",
        max_new_tokens=128,
        do_sample=True,
        temperature=0.7,
        model_kwargs={"stream": False},
        client=InferenceClient(timeout=60)
    )
)

# Load persona prompt for moderator
persona_instruction = get_persona_prompt("moderator")

def moderator_node(state: dict) -> dict:
    topic = state.get("topic", "AI will replace most jobs")
    turn = state.get("turn_count", 0)
    history = state.get("history", [])

    # Get last two AI messages (Proponent + Opponent)
    last_turn = [msg for msg in reversed(history) if isinstance(msg, AIMessage)][:2]
    if len(last_turn) < 2:
        return state  

    summary_input = (
        f"{persona_instruction}\n\n"
        f"Debate Topic: {topic}\n\n"
        f"Latest arguments:\n\n"
        f"Proponent:\n{last_turn[1].content}\n\n"
        f"Opponent:\n{last_turn[0].content}\n\n"
        f"Please summarize this round fairly in less than 80 words. Also detect logical fallacies briefly."
    )

    response = llm.invoke([HumanMessage(content=summary_input)])
    summary = response.content

    # Detect fallacies (if any)
    fallacies = detect_fallacies(last_turn[0].content + "\n" + last_turn[1].content)

    final_output = summary
    if fallacies:
        final_output += f"\n\nDetected Logical Fallacies:\n{fallacies}"

    new_history = history + [HumanMessage(content=summary_input), AIMessage(content=final_output)]

    # Return verdict if debate is over
    if turn >= MAX_TURNS:
        verdict_prompt = (
            f"{persona_instruction}\n\n"
            f"Debate Topic: {topic}\n\n"
            f"Based on the full debate transcript, who presented a stronger case and why?\n\n"
            f"Provide a verdict with reasoning. Keep answer under 100 words."
        )
        verdict_response = llm.invoke([HumanMessage(content=verdict_prompt)])
        new_history.append(verdict_response)

        return {
            **state,
            "history": new_history,
            "verdict": verdict_response.content
        }

    return {
        **state,
        "history": new_history
    }

# Conditional router for LangGraph
def should_continue(state: dict) -> str:
    return "end" if state.get("turn_count", 0) >= MAX_TURNS else "continue"