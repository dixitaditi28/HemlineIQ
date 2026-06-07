from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def generate_briefing(hemline_index, mini_score, midi_score, sentiment, unemployment, inflation):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
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

Write a 3-paragraph Bloomberg-style briefing:
1. What the fashion signals are showing right now
2. How they align or conflict with the hard economic data
3. What this combined picture suggests about consumer mood

Be specific with the numbers. Be confident but acknowledge uncertainty. 
Keep it under 200 words."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Use the real numbers you just got
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