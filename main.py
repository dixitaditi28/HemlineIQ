from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import time

from trends import get_trends_data
from economic import get_economic_summary
from news import get_news_data
from insight import generate_briefing

app = FastAPI(
    title="HemlineIQ API",
    description="A live fashion-economic sentiment tracker based on the Hemline Index theory (George Taylor, 1926).",
    version="1.0.0"
)

# Allow React frontend to call this API from any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- Simple in-memory cache ---
_cache = {
    "briefing": {"data": None, "expires_at": None},
    "trends":   {"data": None, "expires_at": None},
    "economic": {"data": None, "expires_at": None},
    "news":     {"data": None, "expires_at": None},
}

CACHE_TTL_SECONDS = 3600  # 1 hour

def _is_fresh(key: str) -> bool:
    entry = _cache[key]
    return entry["data"] is not None and datetime.utcnow() < entry["expires_at"]

def _store(key: str, data: dict):
    _cache[key]["data"] = data
    _cache[key]["expires_at"] = datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)


# --- Routes ---

@app.get("/health")
def health():
    """Quick check that the server is alive."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/trends")
def trends():
    """
    Returns Google Trends data for mini, midi, and maxi skirt search interest,
    plus the computed Hemline Index.
    """
    if _is_fresh("trends"):
        return {"source": "cache", **_cache["trends"]["data"]}
    try:
        data = get_trends_data()
        _store("trends", data)
        return {"source": "live", **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trends fetch failed: {e}")


@app.get("/economic")
def economic():
    """
    Returns Federal Reserve macroeconomic indicators:
    consumer sentiment, unemployment rate, CPI inflation index.
    """
    if _is_fresh("economic"):
        return {"source": "cache", **_cache["economic"]["data"]}
    try:
        data = get_economic_summary()
        _store("economic", data)
        return {"source": "live", **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Economic fetch failed: {e}")


@app.get("/news")
def news():
    """
    Returns NewsAPI fashion headline data: keyword hit counts,
    sentiment score, dominant signal, and top headlines.
    """
    if _is_fresh("news"):
        return {"source": "cache", **_cache["news"]["data"]}
    try:
        data = get_news_data()
        _store("news", data)
        return {"source": "live", **data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News fetch failed: {e}")


@app.get("/briefing")
def briefing():
    """
    Main endpoint. Pulls all three data sources and generates a
    Bloomberg-style AI briefing via Groq (with Gemini fallback).
    Cached for 1 hour to preserve API quota.
    """
    if _is_fresh("briefing"):
        return {"source": "cache", **_cache["briefing"]["data"]}
    try:
        trends_data   = get_trends_data()
        economic_data = get_economic_summary()

        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "hemline_index": trends_data["hemline_index"],
            "mini_score":    trends_data["mini"],
            "midi_score":    trends_data["midi"],
            "maxi_score":    trends_data.get("maxi", None),
            "sentiment":     economic_data["consumer_sentiment"],
            "unemployment":  economic_data["unemployment"],
            "inflation":     economic_data["inflation"],
            "briefing": generate_briefing(
                hemline_index=trends_data["hemline_index"],
                mini_score=trends_data["mini"],
                midi_score=trends_data["midi"],
                sentiment=economic_data["consumer_sentiment"],
                unemployment=economic_data["unemployment"],
                inflation=economic_data["inflation"],
            )
        }

        _store("briefing", result)
        return {"source": "live", **result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Briefing generation failed: {e}")