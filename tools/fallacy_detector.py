import re

# Define fallacy detection patterns
FALLACY_PATTERNS = {
    "Ad Hominem": r"\b(you'?re wrong because you|you can'?t be trusted|your argument is invalid because you)\b",
    "Strawman": r"\b(so what you'?re saying is|if I understand correctly, you believe)\b",
    "Appeal to Emotion": r"\b(think about the children|how would you feel if)\b",
    "False Dilemma": r"\b(either.*or|only two options|there is no other way)\b",
    "Slippery Slope": r"\b(if we allow this.*soon.*will happen)\b",
    "Bandwagon": r"\b(everyone agrees|most people think|all experts say)\b"
}

def detect_fallacies(text: str) -> str:
    """
    Detects logical fallacies in a given text based on predefined regex patterns.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: A newline-separated string of detected fallacies, or an empty string if none.
    """
    detected = []

    for name, pattern in FALLACY_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(name)

    return "\n".join(detected)