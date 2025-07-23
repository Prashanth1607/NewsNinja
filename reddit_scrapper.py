from typing import List
import google.generativeai as genai
import os
import traceback
from utils import *
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from datetime import datetime, timedelta

load_dotenv()


server_params = StdioServerParameters(
    command="npx",
    env={
        "API_TOKEN": os.getenv("BRIGHTDATA_API_TOKEN"),
        "WEB_UNLOCKER_ZONE": os.getenv("BRIGHTDATA_WEB_UNLOCKER_ZONE"),
    },
    args=["@brightdata/mcp"],
)

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_AI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

async def scrape_reddit_topics(topics: List[str]) -> dict[str, dict]:
    """ Process list of topics and return analysis results """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            
            reddit_results = {}
            for topic in topics:
                summary = await process_topic(agent, topic)
                reddit_results[topic] = summary
                await asyncio.sleep(5)  # Maintain rate limiting
                
            return {"reddit_analysis": reddit_results}
        

mcp_limiter = AsyncLimiter(1, 15)

two_weeks_ago = datetime.today() - timedelta(days=14) 
two_weeks_ago_str = two_weeks_ago.strftime('%Y-%m-%d')

async def process_topic(agent, topic: str):
    async with mcp_limiter:
        messages = [
            {
                "role": "system",
                "content": f"""You are a Reddit analysis expert. Use available tools to:
                1. Find top 2 posts about the given topic BUT only after {two_weeks_ago_str}, NOTHING before this date strictly!
                2. Analyze their content and sentiment
                3. Create a summary of discussions and overall sentiment"""
            },
            {
                "role": "user",
                "content": f"""Analyze Reddit posts about '{topic}'. 
                Provide a comprehensive summary including:
                - Main discussion points
                - Key opinions expressed
                - Any notable trends or patterns
                - Summarize the overall narrative, discussion points and also quote interesting comments without mentioning names
                - Overall sentiment (positive/neutral/negative)"""
            }                   
        ]
        
        try:
            response = await agent.ainvoke({"messages": messages})
            return response["messages"][-1].content
        except Exception as e:
            print("Error in /generate-news-audio:", e)
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))