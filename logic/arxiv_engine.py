import requests
import xml.etree.ElementTree as ET
from typing import List
from .engine_base import SearchEngine, Result

class ArxivEngine(SearchEngine):
    def search(self, query: str, limit: int = 10) -> List[Result]:
        url = "http://export.arxiv.org/api/query"
        # ArXiv API expects 'search_query' and 'start'/'max_results'
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # ArXiv returns Atom XML
            root = ET.fromstring(response.content)
            
            # Namespace map usually needed for Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns)
                summary = entry.find('atom:summary', ns)
                link = entry.find('atom:id', ns) # ArXiv ID is a link usually
                
                # Check for PDF link specifically if possible, but ID is the main abstract page
                
                results.append(Result(
                    title=title.text.strip().replace('\n', ' ') if title is not None else "No Title",
                    link=link.text.strip() if link is not None else "",
                    snippet=summary.text.strip().replace('\n', ' ')[:300] + "..." if summary is not None else "",
                    source="ArXiv"
                ))
            return results
        except requests.RequestException as e:
            print(f"Error querying ArXiv: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing ArXiv XML: {e}")
            return []
