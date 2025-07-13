import traceback
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable
from state.debate_state import DebateState
from tools.persona_prompt_node import PersonaPromptTool
from tools.fallacy_detector_node import FallacyDetectorTool
from light_llm import load_llm
from utils.truncate_prompt import truncate_prompt
from utils.prompt_utils import (
    get_moderator_summary_prompt,
    get_moderator_verdict_prompt,
)

MAX_TURNS = 4

# -- LLM setup --
llm = load_llm()

# -- Tool setup --
persona_tool = PersonaPromptTool()
fallacy_tool = FallacyDetectorTool()

@traceable(name="ModeratorNode")
def moderator_node(state: DebateState):
    topic = state.topic
    turn = state.turn_count
    print(f"[Moderator] Running Turn: {turn}")

    history = state.history
    last_turn = [msg for msg in reversed(history) if isinstance(msg, AIMessage)][:2]

    if len(last_turn) < 2:
        print("[Moderator] Not enough AI responses to moderate.")
        return state

    try:
        # -- Tool invocations --
        persona_prompt = persona_tool.invoke({"agent_role": "moderator"})["persona_prompt"]
        fallacies = fallacy_tool.invoke({
            "text": last_turn[0].content + "\n" + last_turn[1].content
        })["fallacies"]

        # -- Summary Prompt --
        summary_prompt = get_moderator_summary_prompt(
            topic=topic,
            proponent=last_turn[1].content,
            opponent=last_turn[0].content,
            persona=persona_prompt,
            fallacies=fallacies,
        )

        summary_prompt = truncate_prompt(summary_prompt)
        response = llm.invoke(summary_prompt)
        content = getattr(response, "content", "").strip()
        if not content:
            raise ValueError("Empty response from LLM")

        state.history += [HumanMessage(content=summary_prompt), AIMessage(content=content)]

        # -- Verdict (if final round) --
        if turn >= MAX_TURNS:
            verdict_prompt = get_moderator_verdict_prompt(topic=topic, persona=persona_prompt)
            verdict_prompt = truncate_prompt(verdict_prompt)
            verdict_response = llm.invoke(verdict_prompt)
            verdict_content = getattr(verdict_response, "content", "").strip()
            state.verdict = verdict_content
            state.history += [HumanMessage(content=verdict_prompt), AIMessage(content=verdict_content)]

        return state

    except Exception as e:
        print(f"[Moderator Node] Exception:\n{traceback.format_exc()}")
        state.error = str(e)
        return state


def should_continue(state: DebateState) -> str:
    print(f"[Router] Turn: {state.turn_count} → ", end="")
    if state.turn_count >= MAX_TURNS:
        print("ENDING debate.")
        return "end"
    print("Continuing debate.")
    return "continue"