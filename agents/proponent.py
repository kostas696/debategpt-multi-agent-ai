import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from huggingface_hub.inference._client import InferenceClient
from tools.persona_prompt_tool import get_persona_prompt
from tools.tavily_search_tool import tavily_tool

# Use a lighter model and reduce output
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

persona_instruction = get_persona_prompt("proponent")

def proponent_node(state: dict) -> dict:
    topic = state.get("topic", "AI will replace most jobs")
    turn = state.get("turn_count", 0)
    last_history = state.get("history", [])

    evidence = tavily_tool(f"Arguments supporting: {topic}")

    prompt = (
        f"{persona_instruction}\n\n"
        f"Debate Topic: {topic}\n\n"
        f"Please present strong arguments in favor of the topic, using reasoning and supporting evidence.\n\n"
        f"{evidence}\n\n"
        f"Keep your answer concise and under 100 words."
    )

    messages = [HumanMessage(content=prompt)]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        print(f"Error in Proponent Node: {e}")
        return {**state, "error": str(e)}

    new_history = last_history + [messages[0], response]

    return {
        **state,
        "history": new_history,
        "last_speaker": "proponent",
        "turn_count": turn + 1,
    }