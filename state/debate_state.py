from typing import List, Literal, Optional, TypedDict, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class DebateState(TypedDict, total=False):
    topic: str
    history: List[BaseMessage]
    turn_count: int
    last_speaker: Literal["proponent", "opponent"]
    verdict: Optional[str]