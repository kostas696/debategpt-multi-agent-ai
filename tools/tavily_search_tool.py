# tools/tavily_search_tool.py

import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY)


def tavily_tool(query: str, max_results: int = 3) -> str:
    """
    Fetches top relevant results for a given query using Tavily Search API
    and returns them as a formatted string.
    """
    if not TAVILY_API_KEY:
        return "Tavily API key not found. Skipping evidence retrieval."

    try:
        results = client.search(query=query, search_depth="advanced", max_results=max_results)

        if not results or "results" not in results:
            return "No relevant results found."

        evidence = "\n".join(
            f"{item['title']} - {item['url']}\n{item['content']}\n"
            for item in results["results"]
        )
        return f"Relevant research and sources:\n\n{evidence}"

    except Exception as e:
        return f"Error fetching Tavily results: {e}"
