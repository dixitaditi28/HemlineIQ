readme_content = """# 👗 HemlineIQ: Fashion-Economic Sentiment Tracker

**HemlineIQ** is a live web application that modernizes economist George Taylor's 1926 "Hemline Index" theory. It programmatically correlates fashion search trends (specifically the popularity of mini vs. midi/maxi skirts) with hard macroeconomic data (consumer sentiment, unemployment, inflation) to explore whether fashion acts as a leading indicator of public economic sentiment.

The conceptual foundation of this project is rooted in historical economic theories and sparked by modern fashion journalism, specifically exploring the question: [*Does the Midi Skirt Trend Predict a Recession?*](https://www.voguearabia.com/article/does-the-midi-skirt-trend-predict-a-recession)

## 🛠️ Tech Stack & Tooling
- **Backend:** Python, FastAPI
- **Frontend:** React, Recharts
- **Hosting:** Hugging Face Spaces
- **Data Integrations:** - `pytrends` (Google Trends)
  - Federal Reserve Economic Data (`fredapi`)
  - NewsAPI (Fashion headlines)
  - Groq API (LLM Insight generation)

## 📂 Current Project Structure
Files successfully generated.

```text
hemlineiq/
├── app.py              # FastAPI backend (Pending)
├── trends.py           # pytrends Google Trends fetcher (Completed)
├── economic.py         # FRED API fetcher (Completed)
├── news.py             # NewsAPI scraper (Pending)
├── insight.py          # Groq LLM insight generator (Pending)
├── requirements.txt    # Project dependencies
├── .env                # Secure environment variables (Not tracked in git)
└── README.md