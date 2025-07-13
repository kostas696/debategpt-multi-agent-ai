from tools.persona_prompt_node import PersonaPromptTool

if __name__ == "__main__":
    tool = PersonaPromptTool()
    print(tool.invoke({"agent_role": "opponent"}))
