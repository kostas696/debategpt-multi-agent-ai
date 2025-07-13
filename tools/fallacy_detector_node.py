from typing import TypedDict
from langchain_core.runnables import Runnable
from tools.fallacy_detector import detect_fallacies

class FallacyInput(TypedDict):
    text: str

class FallacyOutput(TypedDict):
    fallacies: str

class FallacyDetectorTool(Runnable):
    def invoke(self, input: FallacyInput, config=None, **kwargs) -> FallacyOutput:
        fallacy_list = detect_fallacies(input["text"])
        return {"fallacies": fallacy_list}
