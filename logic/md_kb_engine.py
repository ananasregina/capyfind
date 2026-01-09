import os
import requests
from typing import List, Optional
from .engine_base import SearchEngine, Result


class MdKbEngine(SearchEngine):
    """
    Search engine for md-kb JSON-RPC server.

    Connects to a running md-kb JSON-RPC server to perform semantic search
    on markdown documents.
    """

    def __init__(self, url: Optional[str] = None):
        """
        Initialize the md-kb search engine.

        Args:
            url: JSON-RPC server URL (default: from MDKB_JSONRPC_URL env var or http://127.0.0.1:8000/)
        """
        self.url: str = url or os.environ.get("MDKB_JSONRPC_URL", "http://127.0.0.1:8023/")
        if not self.url.endswith("/"):
            self.url += "/"

    def search(self, query: str, limit: int = 10) -> List[Result]:
        """
        Perform semantic search using md-kb JSON-RPC server.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List[Result]: Search results from the knowledge base
        """
        if not query:
            return []

        # Build JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "method": "search",
            "params": {
                "query": query,
                "limit": limit,
                "max_distance": 0.5
            },
            "id": 1
        }

        try:
            response = requests.post(self.url, json=request, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for JSON-RPC errors
            if "error" in data:
                print(f"md-kb JSON-RPC error: {data['error']}")
                return []

            # Parse results
            results = []
            if "result" in data and data["result"]:
                for doc in data["result"]:
                    # Create snippet from content (first 300 chars)
                    content = doc.get("content", "")
                    snippet = content[:300].replace("\n", " ")
                    if len(content) > 300:
                        snippet += "..."

                    # Use file path as title, strip common prefixes
                    file_path = doc.get("file_path", "Unknown")
                    title = file_path

                    # Convert distance to similarity score (lower distance = higher similarity)
                    distance = doc.get("distance")
                    if distance is not None:
                        similarity = 1.0 - distance
                    else:
                        similarity = 0.0

                    results.append(Result(
                        title=title,
                        link=f"file://{file_path}",
                        snippet=snippet,
                        source=f"MD-KB ({similarity:.2%} match)"
                    ))

            return results

        except requests.exceptions.ConnectionError as e:
            print(f"Warning: Could not connect to md-kb server at {self.url}: {e}")
            return []
        except requests.exceptions.Timeout as e:
            print(f"Warning: Timeout connecting to md-kb server at {self.url}: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error querying md-kb server: {e}")
            return []
        except Exception as e:
            print(f"Warning: Unexpected error with md-kb: {e}")
            return []
