import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

# --- Keyword taxonomy ---

HEMLINE_KEYWORDS = {
    "mini": ["mini skirt", "miniskirt", "short skirt", "micro skirt", "short hemline"],
    "midi": ["midi skirt", "midi dress", "midi length", "below-the-knee"],
    "maxi": ["maxi skirt", "maxi dress", "floor-length", "long hemline", "long skirt"],
    "luxury": ["luxury fashion", "designer bag", "couture", "high-end fashion", "Hermès", "Chanel"],
}

ECONOMIC_SENTIMENT_KEYWORDS = {
    "optimism": ["consumer confidence", "spending surge", "retail boom", "economic growth", "bull market"],
    "pessimism": ["recession", "inflation", "layoffs", "downturn", "bear market", "economic anxiety"],
}

# --- Fetch articles ---

def fetch_fashion_news(days_back: int = 7, page_size: int = 30) -> list[dict]:
    """
    Fetch recent fashion headlines from NewsAPI.
    Uses the free tier (100 req/day). Returns a list of article dicts.
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found. Add it to your .env file.")

    from_date = (datetime.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    params = {
        "q": "fashion skirt dress hemline style trend",
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": page_size,
        "from": from_date,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    articles = response.json().get("articles", [])
    return articles


# --- Keyword extraction ---

def extract_keyword_hits(articles: list[dict]) -> dict:
    """
    Scans article titles + descriptions for hemline and economic keywords.
    Returns counts per category.
    """
    hits = {
        "mini": 0,
        "midi": 0,
        "maxi": 0,
        "luxury": 0,
        "optimism": 0,
        "pessimism": 0,
    }

    for article in articles:
        text = " ".join([
            article.get("title") or "",
            article.get("description") or "",
        ]).lower()

        for category, terms in HEMLINE_KEYWORDS.items():
            if any(term.lower() in text for term in terms):
                hits[category] += 1

        for category, terms in ECONOMIC_SENTIMENT_KEYWORDS.items():
            if any(term.lower() in text for term in terms):
                hits[category] += 1

    return hits


# --- Sentiment score ---

def compute_news_sentiment(hits: dict) -> dict:
    """
    Derives a simple fashion-economic sentiment score from keyword hits.

    Hemline signal:
      - More mini/luxury mentions → economic optimism signal
      - More maxi mentions → economic caution signal

    Returns a score from -1.0 (bearish/long hems) to +1.0 (bullish/short hems),
    plus a dominant_signal label.
    """
    bullish = hits.get("mini", 0) + hits.get("luxury", 0) + hits.get("optimism", 0)
    bearish = hits.get("maxi", 0) + hits.get("pessimism", 0)
    total = bullish + bearish

    if total == 0:
        score = 0.0
    else:
        score = round((bullish - bearish) / total, 3)

    if score > 0.2:
        signal = "bullish"
    elif score < -0.2:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "sentiment_score": score,
        "dominant_signal": signal,
        "bullish_hits": bullish,
        "bearish_hits": bearish,
    }


# --- Top headlines ---

def get_top_headlines(articles: list[dict], n: int = 5) -> list[str]:
    """Returns the top-n article titles for use in LLM context."""
    return [
        article["title"]
        for article in articles[:n]
        if article.get("title")
    ]


# --- Main entry point ---

def get_news_data() -> dict:
    """
    Full pipeline: fetch → extract → score.
    Returns a structured dict ready to pass into insight.py.
    """
    articles = fetch_fashion_news()
    hits = extract_keyword_hits(articles)
    sentiment = compute_news_sentiment(hits)
    headlines = get_top_headlines(articles)

    return {
        "article_count": len(articles),
        "keyword_hits": hits,
        "sentiment": sentiment,
        "top_headlines": headlines,
    }


if __name__ == "__main__":
    import json
    data = get_news_data()
    print(json.dumps(data, indent=2))