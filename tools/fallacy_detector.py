# tools/fallacy_detector.py

import re

FALLACY_PATTERNS = {
    "Ad Hominem": r"(you're wrong because you|you can't be trusted|your argument is invalid because you)",
    "Strawman": r"(so what you're saying is|if I understand correctly, you believe)",
    "Appeal to Emotion": r"(think about the children|how would you feel if)",
    "False Dilemma": r"(either.*or|only two options|there is no other way)",
    "Slippery Slope": r"(if we allow this.*soon.*will happen)",
    "Bandwagon": r"(everyone agrees|most people think|all experts say)",
}


def detect_fallacies(text: str) -> str:
    """
    Detects basic logical fallacies in a text using regex pattern matching.
    Returns a list of identified fallacies, or an empty string if none found.
    """
    detected = []

    for name, pattern in FALLACY_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(f"{name}")

    return "\n".join(detected) if detected else ""
