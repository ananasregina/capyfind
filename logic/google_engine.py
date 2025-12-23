import os
import requests
from typing import List
from .engine_base import SearchEngine, Result

class GoogleEngine(SearchEngine):
    def search(self, query: str, limit: int = 10) -> List[Result]:
        api_key = os.environ.get("GOOGLE_CSE_API_KEY")
        engine_id = os.environ.get("GOOGLE_CSE_ENGINE_ID")
        
        if not api_key or not engine_id:
            print("Warning: GOOGLE_CSE_API_KEY or GOOGLE_CSE_ENGINE_ID not set.")
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": engine_id,
            "q": query,
            "num": limit
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    results.append(Result(
                        title=item.get("title", "No Title"),
                        link=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        source="Google"
                    ))
            return results
        except requests.RequestException as e:
            print(f"Error querying Google: {e}")
            return []
