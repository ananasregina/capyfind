import concurrent.futures
from typing import List
from .engine_base import SearchEngine, Result

class SearchAggregator:
    def __init__(self, engines: List[SearchEngine]):
        self.engines = engines

    def search(self, query: str, limit: int = 10) -> List[Result]:
        if not self.engines:
            return []

        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # key is future, value is engine name (for debugging if needed)
            future_to_engine = {
                executor.submit(engine.search, query, limit): engine 
                for engine in self.engines
            }
            
            for future in concurrent.futures.as_completed(future_to_engine):
                try:
                    engine_results = future.result()
                    results.extend(engine_results)
                except Exception as exc:
                    print(f"Engine generated an exception: {exc}")

        # Simple separate merge: just list them all. 
        # INSTRUCTIONS said: "We can either merge the results of multiple engines, or we can show them separately, it's up to you."
        # Interleaving might be nice but appending is simpler and strictly signal-based.
        # Let's verify instructions again... "filtered out" noise.
        # Minimal processing: just return the raw list.
        return results
