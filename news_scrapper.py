from utils import *
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
import os
from typing import Dict, List
import asyncio

load_dotenv()

class NewsScraper:
    _rate_limiter = AsyncLimiter(5, 1) # 5 requests/second

    async def scrape_news(self, topics: List[str]) -> Dict[str, str]:
        """ Scrape and analyze news articles"""
        results = {}

        for topic in topics:
            async with self._rate_limiter:
                try:
                    urls = generate_news_urls_to_scrape([topic])
                    search_html = scrape_with_brightdata(urls[topic])
                    clean_text = clean_html_to_text(search_html)
                    headlines = extract_headlines(clean_text)
                    summary = summarize_with_gemini_news_script(
                        api_key=os.getenv("GOOGLE_GEMINI_AI_API_KEY"),
                        headlines=headlines
                    )
                    results[topic] = summary

                except Exception as e:
                    results[topic] = f"Error: {str(e)}"
                await asyncio.sleep(1)
        return {"news_analysis" : results}