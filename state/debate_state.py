from dataclasses import dataclass, field
from typing import List, Optional, Literal
from langchain_core.messages import BaseMessage

@dataclass
class DebateState:
    topic: str = "AI will replace most jobs"
    history: List[BaseMessage] = field(default_factory=list)
    turn_count: int = 0
    last_speaker: Optional[Literal["proponent", "opponent"]] = None
    verdict: Optional[str] = None
    error: Optional[str] = None  
    debug_log: List[str] = field(default_factory=list)  