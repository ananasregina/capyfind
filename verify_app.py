import unittest
from app import app
from logic.arxiv_engine import ArxivEngine
from logic.tavily_engine import TavilyEngine

class TestCapyfind(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CAPYFIND', response.data)
        self.assertIn(b'Engines:', response.data)

    def test_search_no_query(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a search query', response.data)

    def test_arxiv_engine_integration(self):
        # Real network call to ArXiv (might fail if no internet, but usually fine)
        engine = ArxivEngine()
        results = engine.search("quantum", limit=1)
        if results:
            print(f"\n[ArXiv Test] Found: {results[0].title}")
            self.assertEqual(results[0].source, "ArXiv")
        else:
            print("\n[ArXiv Test] No results or network error")

    def test_tavily_engine_integration(self):
        # Real network call to Tavily (requires API key)
        engine = TavilyEngine()
        results = engine.search("capybara", limit=1)
        if results:
            print(f"\n[Tavily Test] Found: {results[0].title}")
            self.assertEqual(results[0].source, "Tavily")
        else:
            print("\n[Tavily Test] No results or network error (or API key not set)")

if __name__ == '__main__':
    unittest.main()
