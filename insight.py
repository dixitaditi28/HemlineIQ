from groq import Groq
from dotenv import load_dotenv
from news import get_news_data  # NEW
import os

load_dotenv()

def generate_briefing(hemline_index, mini_score, midi_score, sentiment, unemployment, inflation):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    news = get_news_data()  # NEW
    news_signal = news['sentiment']['dominant_signal']
    news_score = news['sentiment']['sentiment_score']
    news_hits = news['keyword_hits']
    news_headlines = "\n".join(f"- {h}" for h in news['top_headlines'])

    prompt = f"""You are a financial analyst who specializes in alternative economic indicators, 
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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350  # bumped slightly to fit the extra paragraph
    )

    return response.choices[0].message.content

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