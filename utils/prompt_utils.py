# prompt_utils.py

# Toggle to switch prompt styles based on the model size
USE_TINY_MODEL = True  # Set to False if using larger instruction-tuned models like Mistral

def get_proponent_prompt(topic: str) -> str:
    if USE_TINY_MODEL:
        return (
            f"Debate topic: {topic}\n"
            f"Proponent's argument (keep it short):"
        )
    else:
        return (
            f"<s>[INST] You are the proponent in a debate on the topic: '{topic}'. "
            f"Provide a clear argument supporting the topic. Keep it concise. [/INST]</s>"
        )

def get_opponent_prompt(topic: str, previous_argument: str) -> str:
    if USE_TINY_MODEL:
        return (
            f"Debate topic: {topic}\n"
            f"Proponent's argument: {previous_argument}\n"
            f"Opponent's counterargument (keep it short):"
        )
    else:
        return (
            f"<s>[INST] You are the opponent in a debate on the topic: '{topic}'. "
            f"The proponent said: '{previous_argument}'. Rebut the argument concisely. [/INST]</s>"
        )

def get_moderator_prompt(topic: str, proponent: str, opponent: str) -> str:
    if USE_TINY_MODEL:
        return (
            f"Debate topic: {topic}\n"
            f"Proponent said: {proponent}\n"
            f"Opponent said: {opponent}\n"
            f"Moderator's summary (keep it short):"
        )
    else:
        return (
            f"<s>[INST] You are the moderator of a debate on the topic: '{topic}'. "
            f"The proponent argued: '{proponent}', and the opponent replied: '{opponent}'. "
            f"Briefly summarize and conclude the round. [/INST]</s>"
        )

def get_moderator_summary_prompt(topic: str, proponent: str, opponent: str, persona: str, fallacies: str) -> str:
    return (
        f"{persona}\n\n"
        f"Topic: {topic}\n"
        f"Proponent said: {proponent}\n"
        f"Opponent said: {opponent}\n\n"
        f"Summarize this debate turn in under 80 words.\n"
        f"Detected fallacies: {fallacies if fallacies else 'None'}"
    )

def get_moderator_verdict_prompt(topic: str, persona: str) -> str:
    return (
        f"{persona}\n\n"
        f"Topic: {topic}\n"
        f"Who made the stronger case overall? Reply in under 100 words."
    )