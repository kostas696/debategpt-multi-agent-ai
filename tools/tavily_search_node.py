from typing import TypedDict, Optional
from langchain_core.runnables import Runnable
from tools.tavily_search_tool import tavily_tool

class TavilyInput(TypedDict):
    query: str
    max_results: Optional[int]

class TavilyOutput(TypedDict):
    evidence: str

class TavilySearchTool(Runnable):
    def invoke(self, input: TavilyInput, config=None, **kwargs) -> TavilyOutput:
        evidence = tavily_tool(query=input["query"], max_results=input.get("max_results", 3))
        return {"evidence": evidence}