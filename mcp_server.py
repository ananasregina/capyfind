from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from typing import List, Optional

# Load env variables
load_dotenv()

from logic.google_engine import GoogleEngine
from logic.arxiv_engine import ArxivEngine
from logic.tavily_engine import TavilyEngine
from logic.md_kb_engine import MdKbEngine
from logic.aggregator import SearchAggregator

# Initialize FastMCP server
mcp = FastMCP("Capyfind")

@mcp.tool()
def capy_find(query: str, engines: Optional[List[str]] = None, limit: int = 10) -> str:
    """
    Search the web with the infinite wisdom of the Capybara.
    
    Args:
        query: The search query.
        engines: List of engines to use (google, arxiv, tavily, mdkb). Defaults to all.
        limit: Max results per engine.
    """
    available_engines = {
        "google": GoogleEngine(),
        "arxiv": ArxivEngine(),
        "tavily": TavilyEngine(),
        "mdkb": MdKbEngine()
    }
    
    selected_engines = []
    if engines:
        for e in engines:
            if e in available_engines:
                selected_engines.append(available_engines[e])
    else:
        selected_engines = list(available_engines.values())
        
    aggregator = SearchAggregator(selected_engines)
    results = aggregator.search(query, limit=limit)
    
    if not results:
        return "No results found."
    
    formatted_results = []
    for res in results:
        formatted_results.append(f"### {res.title}\nSource: {res.source}\nLink: {res.link}\n\n{res.snippet}\n---")
        
    return "\n".join(formatted_results)

def format_results(results) -> str:
    if not results:
        return "No results found."
    formatted_results = []
    for res in results:
        formatted_results.append(f"### {res.title}\nLink: {res.link}\n\n{res.snippet}\n---")
    return "\n".join(formatted_results)

if __name__ == "__main__":
    mcp.run()
