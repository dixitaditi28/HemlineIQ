**HemlineIQ: Fashion-Economic Sentiment Tracker**

**The Idea**

The project started from a casual observation about fashion trends and economic mood — that what people wear might reflect how they feel about the economy. This turned out to be a real, documented economic theory called the Hemline Index, first proposed by economist George Taylor in 1926. The theory states that skirt lengths shorten during economic growth and lengthen during downturns. It sits alongside other fashion-based economic indicators like the Lipstick Index and the High Heel Index. A 2025 cross-country study across 30 nations found a statistically significant inverse relationship between economic optimism and hemline length, so there's actual academic backing for this.

The goal was to build something more original than a standard API-aggregator portfolio project — something with a real thesis, visual storytelling potential, and an explainable hook for non-technical people like interviewers or journalists.

---

**What HemlineIQ Is**

A live fashion-economic sentiment tracker. It pulls fashion trend signals from Google Trends (how much people are searching for mini skirts vs midi skirts), maps them against real macroeconomic data from the Federal Reserve (consumer confidence, unemployment, inflation), and uses an AI model to generate a Bloomberg-style analyst briefing that interprets what the combined signals mean.

It is a live web application that modernizes economist George Taylor's 1926 "Hemline Index" theory. It programmatically correlates fashion search trends (specifically the popularity of mini vs. midi/maxi skirts) with hard macroeconomic data (consumer sentiment, unemployment, inflation) to explore whether fashion acts as a leading indicator of public economic sentiment.

The conceptual foundation of this project is rooted in historical economic theories and sparked by modern fashion journalism, specifically exploring the question: [*Do Women Fashion Trends Predict a Recession?*](https://www.voguearabia.com/article/does-the-midi-skirt-trend-predict-a-recession)

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