from tools.tavily_search_node import TavilySearchTool

if __name__ == "__main__":
    tool = TavilySearchTool()
    result = tool.invoke({"query": "AI and employment"})
    print(result["evidence"])
