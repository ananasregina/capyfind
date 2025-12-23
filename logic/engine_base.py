from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Result:
    title: str
    link: str
    snippet: str
    source: str

class SearchEngine(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Result]:
        """
        Perform a search and return a list of Result objects.
        """
        pass
