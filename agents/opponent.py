import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from tools.persona_prompt_tool import get_persona_prompt
from tools.tavily_search_tool import tavily_tool

from langchain_community.chat_models import ChatHuggingFace

llm = ChatHuggingFace(
    repo_id=os.getenv("LLM_MODEL", "HuggingFaceH4/zephyr-7b-beta"),
    temperature=0.7,
    streaming=True
)

persona_instruction = get_persona_prompt("opponent")

def opponent_node(state: dict) -> dict:
    topic = state.get("topic", "AI will replace most jobs")
    turn = state.get("turn_count", 0)
    last_history = state.get("history", [])

    # Extract the last argument (Proponent's statement)
    proponent_argument = ""
    for msg in reversed(last_history):
        if isinstance(msg, AIMessage):
            proponent_argument = msg.content
            break

    evidence = tavily_tool(f"Counter arguments to: {topic}")

    messages = [
        HumanMessage(
            content=(
                f"{persona_instruction}\n\n"
                f"Debate Topic: {topic}\n\n"
                f"Your opponent argued: \"{proponent_argument}\"\n\n"
                f"Please rebut their claim with counterarguments, evidence, and reasoning.\n\n"
                f"{evidence}"
            )
        )
    ]

    response = llm.invoke(messages)

    # Update state
    new_history = last_history + [messages[0], response]

    return {
        **state,
        "history": new_history,
        "last_speaker": "opponent",
        "turn_count": turn + 1
    }
