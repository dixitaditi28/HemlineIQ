# HemlineIQ: Fashion-Economic Sentiment Tracker

> *"Skirt lengths rise with the stock market and fall with recessions."*
> — George Taylor, economist, 1926

---

## The Idea

The project started from a casual observation about fashion trends and economic mood — that what people wear might reflect how they feel about the economy. This turned out to be a real, documented economic theory called the **Hemline Index**, first proposed by economist George Taylor in 1926. The theory states that skirt lengths shorten during economic growth and lengthen during downturns. It sits alongside other fashion-based economic indicators like the Lipstick Index and the High Heel Index.

A [2025 cross-country study across 30 nations](https://www.researchgate.net) found a statistically significant inverse relationship between economic optimism and hemline length — so there's genuine academic backing for this.

The goal was to build something more original than a standard API-aggregator portfolio project — something with a real thesis, visual storytelling potential, and an explainable hook for non-technical people like interviewers or journalists.

The conceptual foundation was also sparked by modern fashion journalism, specifically the question: [*Do Women's Fashion Trends Predict a Recession?*](https://www.voguearabia.com/article/does-the-midi-skirt-trend-predict-a-recession)

---

## What HemlineIQ Is

A **live fashion-economic sentiment tracker**. It pulls fashion trend signals from Google Trends (how much people are searching for mini vs midi vs maxi skirts), maps them against real macroeconomic data from the Federal Reserve (consumer confidence, unemployment, inflation), scrapes fashion news headlines, and uses an AI model to generate a Bloomberg-style analyst briefing interpreting what the combined signals mean.

The core signal — the **Hemline Index** — is calculated as:

```
Hemline Index = mini skirt search interest − midi skirt search interest
```

Positive = people trending toward shorter hemlines = historically an optimism signal.
Negative = people trending toward longer hemlines = historically a caution signal.

---

## Dashboard

![HemlineIQ Dashboard](screenshots/dashboard.png)

The dashboard shows the live Hemline Index, mini/midi/maxi search interest scores, Federal Reserve macroeconomic indicators, and an AI-generated Bloomberg-style briefing — all updated in real time.

---

## How It Works

```
Google Trends (pytrends)
        ↓
  trends.py → hemline_index, mini/midi/maxi scores
        ↓
Federal Reserve (fredapi)          NewsAPI
        ↓                               ↓
  economic.py → sentiment,        news.py → headlines,
  unemployment, CPI               keyword hits, sentiment score
        ↓                               ↓
              insight.py (Groq LLM → Gemini fallback)
                        ↓
              Bloomberg-style analyst briefing
                        ↓
              main.py (FastAPI backend)
                        ↓
              index.html (live dashboard)
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data — Fashion Trends | `pytrends` (Google Trends, free, no key) |
| Data — Macroeconomic | `fredapi` (Federal Reserve FRED API, free) |
| Data — News | NewsAPI (free tier, 100 req/day) |
| LLM — Primary | Groq API (`llama-3.3-70b-versatile`) |
| LLM — Fallback | Google Gemini (`gemini-2.0-flash`) |
| Backend | Python, FastAPI, uvicorn |
| Frontend | HTML, Tailwind CSS, Space Mono + Playfair Display |
| Environment | python-dotenv |

---

## Project Structure

```
hemlineiq/
├── trends.py              ← Google Trends fetcher + Hemline Index calculator
├── economic.py            ← FRED API fetcher (sentiment, unemployment, CPI)
├── news.py                ← NewsAPI scraper + keyword extractor + sentiment scorer
├── insight.py             ← LLM briefing generator (Groq primary, Gemini fallback)
├── main.py                ← FastAPI backend (5 endpoints, 1hr in-memory cache)
├── index.html             ← Frontend dashboard
├── requirements.txt
├── .env                   ← API keys (not tracked in git)
├── .gitignore
└── README.md
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Server liveness check |
| `GET /trends` | Google Trends hemline data |
| `GET /economic` | Federal Reserve macroeconomic indicators |
| `GET /news` | Fashion headlines + sentiment score |
| `GET /briefing` | Full pipeline — all sources + AI briefing (cached 1hr) |
| `GET /docs` | Auto-generated Swagger UI |

---

## Running Locally

**1. Clone and set up environment**
```bash
git clone https://github.com/dixitaditi28/hemlineiq.git
cd hemlineiq
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

**2. Add your API keys to `.env`**
```
FRED_API_KEY=your_fred_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
NEWS_API_KEY=your_newsapi_key
```

Get them free at:
- FRED: [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)
- Groq: [console.groq.com](https://console.groq.com)
- Gemini: [aistudio.google.com](https://aistudio.google.com)
- NewsAPI: [newsapi.org](https://newsapi.org)

**3. Start the backend**
```bash
uvicorn main:app --reload
```

**4. Open the dashboard**

Open `index.html` in your browser. The dashboard will connect to `http://127.0.0.1:8000` automatically.

---

## Academic Foundation

- **George Taylor (1926)** — original Hemline Index theory
- **Marjolein van Baardwijk & Philip Hans Franses (2010)** — *"The Hemline and the Economy: Is There Any Match?"* Econometric Institute, Erasmus University Rotterdam
- **2025 cross-country study** — statistically significant inverse relationship between economic optimism and hemline length across 30 nations
- Vogue Arabia — [*Do Women's Fashion Trends Predict a Recession?*](https://www.voguearabia.com/article/does-the-midi-skirt-trend-predict-a-recession)

---

## What's Next

- [ ] Historical `/trends/history` endpoint for real sparkline data
- [ ] Deploy to Hugging Face Spaces
- [ ] Reddit API integration (`r/femalefashionadvice`, `r/streetwear`)
- [ ] Time-series chart overlaying Hemline Index against consumer sentiment

---

*Built by Aditi Dixit · 2026*

