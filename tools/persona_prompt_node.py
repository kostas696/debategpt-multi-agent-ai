from typing import TypedDict
from langchain_core.runnables import Runnable
from tools.persona_prompt_tool import get_persona_prompt

class PersonaInput(TypedDict):
    agent_role: str

class PersonaOutput(TypedDict):
    persona_prompt: str

class PersonaPromptTool(Runnable):
    def invoke(self, input: PersonaInput, config=None, **kwargs) -> PersonaOutput:
        prompt = get_persona_prompt(input["agent_role"])
        return {"persona_prompt": prompt}