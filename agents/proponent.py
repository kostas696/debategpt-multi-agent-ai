import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from tools.persona_prompt_tool import get_persona_prompt
from tools.tavily_search_tool import tavily_tool

# Load your LLM
from langchain_community.chat_models import ChatHuggingFace

llm = ChatHuggingFace(
    repo_id=os.getenv("LLM_MODEL", "HuggingFaceH4/zephyr-7b-beta"),
    temperature=0.7,
    streaming=True
)

# Define the Proponent persona
persona_instruction = get_persona_prompt("proponent")

# Define Proponent node
def proponent_node(state: dict) -> dict:
    topic = state.get("topic", "AI will replace most jobs")
    turn = state.get("turn_count", 0)

    # Use Tavily to fetch some current data
    evidence = tavily_tool(f"{topic} arguments supporting the position")

    messages = [
        HumanMessage(content=f"{persona_instruction}\n\nDebate Topic: {topic}\n\nYou are making the opening argument for the proposition. Use facts if possible.\n\n{evidence}")
    ]

    response = llm.invoke(messages)

    # Update history and state
    new_history = state.get("history", []) + [messages[0], response]

    return {
        **state,
        "history": new_history,
        "last_speaker": "proponent",
        "turn_count": turn + 1
    }
