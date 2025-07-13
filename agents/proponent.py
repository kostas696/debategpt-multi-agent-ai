import traceback
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable
from light_llm import load_llm
from tools.persona_prompt_node import PersonaPromptTool
from tools.tavily_search_node import TavilySearchTool
from utils.truncate_prompt import truncate_prompt
from utils.prompt_utils import get_proponent_prompt

# -- LLM setup --
llm = load_llm()

# -- ToolNode instances --
persona_tool = PersonaPromptTool()
tavily_tool = TavilySearchTool()

@traceable(name="ProponentNode")
def proponent_node(state):
    topic = state.topic
    turn = state.turn_count
    print(f"[Proponent] Running Turn: {turn}")

    try:
        persona_prompt = persona_tool.invoke({"agent_role": "proponent"})["persona_prompt"]
        evidence = tavily_tool.invoke({"query": f"Arguments supporting: {topic}"})["evidence"]

        prompt = get_proponent_prompt(topic)
        full_prompt = f"{persona_prompt}\n\n{prompt}\n\n{evidence}"
        full_prompt = truncate_prompt(full_prompt)

        response = llm.invoke([HumanMessage(content=full_prompt)])

        if not response or not hasattr(response, "content"):
            raise ValueError("Empty or invalid response from LLM")

        state.history += [HumanMessage(content=full_prompt), AIMessage(content=response.content)]
        state.last_speaker = "proponent"
        state.turn_count = turn + 1
        return state

    except Exception as e:
        print(f"[Proponent Node] Exception:\n{traceback.format_exc()}")
        state.error = str(e)
        return state