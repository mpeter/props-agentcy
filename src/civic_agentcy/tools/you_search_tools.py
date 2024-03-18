import os
import json
import requests
from crewai_tools import BaseTool

you_api_key = os.getenv("YOU_API_KEY")

# YouSearch = web search tool
# YouSummarize = summarize search results
# YouFetchRaw = fetch raw search results
# YouSearchAISnippets = search AI-generated snippets
# YouLLMSearch = search with LLM
# YouNewsSearch = search with News

class YouSearch(BaseTool):
    name: str = "You Search"
    description: str = "Performs a web search using You.com's API."

    def _run(self, query: str) -> str:
        url = "https://api.ydc-index.io/search"
        querystring = {"query": query, "num_web_results": 10}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return json.dumps(data, indent=4)

class YouSummarize(BaseTool):
    name: str = "You Summarize"
    description: str = "Summarizes search results from You.com's API."

    def _run(self, query: str, num_results: int = 10) -> str:
        url = "https://api.ydc-index.io/search"
        querystring = {"query": query, "num_web_results": num_results}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=querystring)
        results = response.json().get('results', [])
        summaries = "\n\n".join(
            f"Title: {result['title']}\nURL: {result['link']}"
            for result in results
        )
        return summaries

class YouFetchRaw(BaseTool):
    name: str = "Fetch Raw Results"
    description: str = "Fetches raw search results from You.com."

    def _run(self, query: str) -> str:
        url = "https://api.ydc-index.io/search"
        querystring = {"query": query, "num_web_results": 10}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=querystring)
        return json.dumps(response.json(), indent=4)

class YouSearchAISnippets(BaseTool):
    name: str = "AI Snippets Search"
    description: str = "Searches AI-generated snippets."

    def _run(self, query: str) -> str:
        url = "https://api.ydc-index.io/news"
        params = {"q": query}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=params)
        results = response.json().get('articles', [])
        snippets = "\n\n".join(
            f"Title: {article['title']}\nDescription: {article['description']}\nURL: {article['url']}"
            for article in results
        )
        return snippets

class YouLLMSearch(BaseTool):
    name: str = "LLM Search"
    description: str = "Leverages the YDC Index RAG API for searching."

    def _run(self, query: str) -> str:
        url = "https://api.ydc-index.io/rag"
        params = {"query": query, "num_web_results": 10}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=params)
        return response.text

class YouNewsSearch(BaseTool):
    name: str = "News Search"
    description: str = "Searches and summarizes AI-generated news articles."

    def _run(self, query: str) -> str:
        url = "https://api.ydc-index.io/news"
        params = {"q": query}
        headers = {"X-API-Key": you_api_key}
        response = requests.get(url, headers=headers, params=params)
        search_results = response.json().get("news", {}).get("results", [])
        summarized_results = "\n\n".join(
            f"Title: {item['title']}\nURL: {item['url']}"
            for item in search_results
        )
        return summarized_results