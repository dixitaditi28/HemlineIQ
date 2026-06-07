**HemlineIQ — Project Log**

**The Idea**

The project started from a casual observation about fashion trends and economic mood — that what people wear might reflect how they feel about the economy. This turned out to be a real, documented economic theory called the Hemline Index, first proposed by economist George Taylor in 1926. The theory states that skirt lengths shorten during economic growth and lengthen during downturns. It sits alongside other fashion-based economic indicators like the Lipstick Index and the High Heel Index. A 2025 cross-country study across 30 nations found a statistically significant inverse relationship between economic optimism and hemline length, so there's actual academic backing for this.

The goal was to build something more original than a standard API-aggregator portfolio project — something with a real thesis, visual storytelling potential, and an explainable hook for non-technical people like interviewers or journalists.

---

**What HemlineIQ Is**

A live fashion-economic sentiment tracker. It pulls fashion trend signals from Google Trends (how much people are searching for mini skirts vs midi skirts), maps them against real macroeconomic data from the Federal Reserve (consumer confidence, unemployment, inflation), and uses an AI model to generate a Bloomberg-style analyst briefing that interprets what the combined signals mean.

The project is named HemlineIQ.

---

**Tech Stack**

- **Python** — primary language for all backend logic
- **pytrends** — unofficial Google Trends API wrapper. Free, no API key needed. Used to pull search volume data for "mini skirt", "midi skirt", "maxi skirt", "mini dress" over the last 5 years in the US. The core signal is the Hemline Index, calculated as mini skirt search score minus midi skirt search score. Positive = people trending toward shorter = historically an optimism signal. Negative = trending toward longer = caution signal.
- **fredapi** — Python wrapper for the Federal Reserve Economic Data (FRED) API. Completely free, requires a free API key from fred.stlouisfed.org. Used to pull three series: Consumer Sentiment (UMCSENT, University of Michigan), Unemployment Rate (UNRATE), and CPI Inflation Index (CPIAUCSL), all from 2020 onward.
- **Groq API** — free-tier LLM API. Used to generate the analyst briefing by passing in all the fashion and economic numbers as a structured prompt. The model used is llama-3.3-70b-versatile (we originally tried llama3-8b-8192 but it had been decommissioned by Groq, so we switched).
- **python-dotenv** — manages API keys securely via a .env file so keys are never hardcoded in scripts.
- **VS Code** — editor. Pylance showed yellow import warnings for fredapi and pytrends but these are cosmetic only — the packages are installed in the venv and the scripts run fine. Fixed by pointing VS Code's Python interpreter to the venv (Ctrl+Shift+P → Python: Select Interpreter → choose the venv path).

---

**Folder Structure (current)**

```
hemlineiq/
├── venv/                  ← virtual environment (not committed to git)
├── .env                   ← API keys (FRED_API_KEY, GROQ_API_KEY)
├── .gitignore
├── trends.py              ← Google Trends fetcher + Hemline Index calculator
├── economic.py            ← FRED API fetcher (sentiment, unemployment, inflation)
├── insight.py             ← Groq LLM briefing generator
├── README.md
└── Phase1_documentation.md
```

---

**What Was Built — Phase 1**

Step 1: Set up the project folder, virtual environment, and installed packages (pytrends, fredapi, pandas, python-dotenv, groq). Created trends.py and economic.py.

Step 2: Ran trends.py successfully. Got real Google Trends data for the last 5 years. Sample of latest data points confirmed the scripts were working and pulling live numbers.

Step 3: Ran economic.py successfully. Got real Federal Reserve data — Consumer Sentiment, Unemployment Rate, CPI.

Step 4: Created insight.py and connected the Groq API. Hit one error (model decommissioned) and fixed it by switching model name from llama3-8b-8192 to llama-3.3-70b-versatile.

Step 5: Got the first working AI briefing generated from real data.

---

**First Real Output (June 7, 2026)**

- Hemline Index: +1 (slight mini skirt lean, weak optimism signal)
- Consumer Sentiment: 49.8/100 (below neutral — people are worried)
- Unemployment: 4.3%
- CPI Inflation Index: 332.4

AI briefing interpretation: Cautiously bullish but conflicted. The fashion signal and low unemployment lean optimistic, but consumer sentiment and inflation tell a more cautious story. The AI correctly identified the tension between these signals.

---

**What's Next (Phase 2)**

- Add NewsAPI scraper to pull fashion headlines from Vogue, WWD, Elle for additional signal
- Wire all three data sources (trends + economic + news) into a single combined data object
- Build the FastAPI backend so data can be served via HTTP endpoints instead of just terminal scripts
- Eventually: React frontend with a Recharts timeline chart overlaying hemline index against consumer sentiment over time, plus the live AI briefing displayed on the dashboard

---

