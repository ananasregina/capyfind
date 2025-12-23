from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

from logic.google_engine import GoogleEngine
from logic.arxiv_engine import ArxivEngine
from logic.aggregator import SearchAggregator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template('index.html', error="Please enter a search query.")
    
    use_google = request.args.get('google') == 'on'
    use_arxiv = request.args.get('arxiv') == 'on'
    
    engines = []
    if use_google:
        engines.append(GoogleEngine())
    if use_arxiv:
        engines.append(ArxivEngine())
        
    if not engines:
         return render_template('index.html', error="Please select at least one search engine.")
    
    aggregator = SearchAggregator(engines)
    results = aggregator.search(query, limit=10)
    
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
