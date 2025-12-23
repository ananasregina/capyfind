import os
import requests
from typing import List
from .engine_base import SearchEngine, Result

class TavilyEngine(SearchEngine):
    def search(self, query: str, limit: int = 10) -> List[Result]:
        api_key = os.environ.get("TAVILY_API_KEY")
        
        if not api_key:
            print("Warning: TAVILY_API_KEY not set.")
            return []

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": limit
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "results" in data:
                for item in data["results"]:
                    results.append(Result(
                        title=item.get("title", "No Title"),
                        link=item.get("url", ""),
                        snippet=item.get("content", ""),
                        source="Tavily"
                    ))
            return results
        except requests.RequestException as e:
            print(f"Error querying Tavily: {e}")
            return []
