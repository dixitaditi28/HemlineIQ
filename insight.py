from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv
from news import get_news_data
import os

load_dotenv()

def build_prompt(hemline_index, mini_score, midi_score, sentiment, unemployment, inflation, news):
    news_signal = news['sentiment']['dominant_signal']
    news_score = news['sentiment']['sentiment_score']
    news_hits = news['keyword_hits']
    news_headlines = (
        "\n".join(f"- {h}" for h in news['top_headlines'])
        if news['top_headlines']
        else "  (news feed unavailable)"
    )

    return f"""You are a financial analyst who specializes in alternative economic indicators, 
particularly fashion trends as economic signals (the Hemline Index theory, first proposed by 
economist George Taylor in 1926).

Here is today's data:

FASHION SIGNALS (Google Trends, US):
- Mini skirt search interest: {mini_score}/100
- Midi skirt search interest: {midi_score}/100
- Hemline Index (mini minus midi): {hemline_index} 
  (positive = people trending toward shorter = historically optimistic signal)
  (negative = people trending toward longer = historically cautious signal)

ECONOMIC DATA (Federal Reserve):
- Consumer Sentiment: {sentiment}/100 (100 = neutral baseline)
- Unemployment Rate: {unemployment}%
- CPI Inflation Index: {inflation}

NEWS SENTIMENT (last 7 days):
- Fashion-economic signal: {news_signal} (score: {news_score})
- Mini mentions: {news_hits['mini']} | Midi: {news_hits['midi']} | Maxi: {news_hits['maxi']} | Luxury: {news_hits['luxury']}
- Top headlines:
{news_headlines}

Write a 3-paragraph Bloomberg-style briefing:
1. What the fashion signals are showing right now
2. How they align or conflict with the hard economic data
3. What the news sentiment and headlines add to the picture — and what this combined view suggests about consumer mood

Be specific with the numbers. Be confident but acknowledge uncertainty. 
Keep it under 250 words."""


def _try_groq(prompt):
    """Primary LLM: Groq (fast, free)."""
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350
    )
    return response.choices[0].message.content


def _try_gemini(prompt):
    """Fallback LLM: Gemini (free, generous limits)."""
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def generate_briefing(hemline_index, mini_score, midi_score, sentiment, unemployment, inflation):
    news = get_news_data()
    prompt = build_prompt(hemline_index, mini_score, midi_score, sentiment, unemployment, inflation, news)

    # Try Groq first, fall back to Gemini if anything goes wrong
    try:
        print("[insight.py] Using Groq...")
        return _try_groq(prompt)
    except Exception as e:
        print(f"[insight.py] Groq failed ({e}) — falling back to Gemini...")

    try:
        return _try_gemini(prompt)
    except Exception as e:
        raise RuntimeError(f"Both LLMs failed. Last error: {e}")


if __name__ == "__main__":
    briefing = generate_briefing(
        hemline_index=1,
        mini_score=6,
        midi_score=5,
        sentiment=49.8,
        unemployment=4.3,
        inflation=332.4
    )
    print("\n=== HEMLINEIQ BRIEFING ===")
    print(briefing)
    print("=========================")