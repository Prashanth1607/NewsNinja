from fastapi import FastAPI, HTTPException, Response
from dotenv import load_dotenv

from models import NewsRequest
from utils import *
from news_scrapper import NewsScraper
from reddit_scrapper import scrape_reddit_topics

app = FastAPI()
load_dotenv()


@app.post("/generate-news-audio")
async def generate_news_audio(request: NewsRequest):
    try:
        results = {}

        # Scrape data
        if request.source_type in ["news", "both"]:
            news_scrapper = NewsScraper()
            results["news"] = await news_scrapper.scrape_news(request.topics)
            print("News results:", results["news"])

        if request.source_type in ["reddit", "both"]:
            results["reddit"] = await scrape_reddit_topics(request.topics)
            print("Reddit results:", results["reddit"])

        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})

        # setup LLM summarizer
        news_summary = generate_broadcast_news(
            api_key=os.getenv("GOOGLE_GEMINI_AI_API_KEY"),
            news_data=news_data,
            reddit_data=reddit_data,
            topics=request.topics
        )
        print("News summary:", news_summary)

        if not news_summary or not isinstance(news_summary, str):
            raise HTTPException(status_code=500, detail="Failed to generate news summary.")

        # convert summary to audio
        audio_path = text_to_audio_elevenlabs_sdk(
            text=news_summary,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            output_dir="audio"
        )
        print("Audio path:", audio_path)

        if not audio_path:
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=news-summary.mp3"}
        )

    except Exception as e:
        print("Error in /generate-news-audio:", e)
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        if "429" in str(e):
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later or upgrade your plan."
            )
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=1234,
        reload=True
    )