HemlineIQ — Project Log
Phase 2 Summary
This phase focused on adding a news data layer to the pipeline, wiring it into the AI briefing generator, and resolving a series of API and dependency issues along the way. By the end of Phase 2, the full three-source pipeline (Google Trends + FRED + NewsAPI) is functional, the AI briefing now incorporates news sentiment and real headlines, and the system has a Groq-primary / Gemini-fallback LLM architecture for resilience.

What Was Built — Phase 2

Step 1: Built news.py
Created a new module to fetch fashion headlines from NewsAPI and extract signal from them. The scraper queries NewsAPI for fashion-related articles from the last 7 days, scans titles and descriptions for hemline keywords (mini, midi, maxi, luxury) and economic sentiment keywords (optimism/pessimism terms), computes a sentiment score between -1.0 (bearish/long hems) and +1.0 (bullish/short hems), and returns a clean structured dict ready to pass into insight.py. The top 5 headlines are also extracted for use in the LLM prompt.
Step 2: Wired news.py into insight.py
Updated insight.py to import and call get_news_data() at the start of generate_briefing(). The news sentiment score, keyword hit counts, and top headlines are all injected into the Groq prompt as a third data block (alongside Google Trends and FRED data). The third paragraph of the Bloomberg-style briefing was updated to specifically address what the news sentiment adds to the picture.


Step 3: Added error resilience to news.py
NewsAPI timed out on first run. After diagnosing (confirmed the site was reachable via Invoke-WebRequest, StatusCode 200), identified the issue as a one-time network hiccup rather than a block. Added a try/except fallback to get_news_data() that returns neutral zero-value data instead of crashing the pipeline when the news fetch fails. Also bumped the request timeout from 10s to 30s.
Step 4: Added Gemini as LLM fallback
Groq threw an organization_restricted error mid-session (account banned due to prior use of multiple accounts). To keep the pipeline running, added Google Gemini (gemini-2.0-flash) as a fallback LLM. The architecture now tries Groq first — if it fails for any reason, it silently falls back to Gemini and logs which model is being used. If both fail, a clear RuntimeError is raised.
Prompt logic was refactored into a standalone build_prompt() function to keep generate_briefing() clean and to make the prompt reusable when the FastAPI backend is built.
Step 5: Resolved Gemini SDK deprecation
The google-generativeai package was deprecated mid-session. Switched to the new google-genai SDK and updated the Gemini client code accordingly (genai.Client + client.models.generate_content). Model name updated to gemini-2.0-flash.
Step 6: Groq reinstated
Contacted Groq support via live chat. Account was reinstated as a one-time exception after explaining the situation. Going forward, only one Groq account (itsdixitaditi@gmail.com) is in use. Final pipeline run confirmed Groq working again — briefing generated successfully from real data.

Problems Encountered
NewsAPI timeout (ReadTimeout after 10s)
First run of news.py timed out. Initially suspected a geo-block (India), ruled out after confirming StatusCode 200 via Invoke-WebRequest. Root cause: one-time network hiccup. Fix: bumped timeout to 30s and added a try/except fallback so the pipeline never crashes on a news failure.
Windows curl alias confusion
Running curl -I https://newsapi.org in PowerShell triggered a prompt for a Uri: parameter instead of running — because PowerShell aliases curl to Invoke-WebRequest, not the real curl binary. Fix: used Invoke-WebRequest -Uri https://newsapi.org -Method Head directly.
Groq organization_restricted error
Groq banned the account mid-session due to prior use of multiple accounts (a ToS violation). Fix: contacted Groq support via live chat, account reinstated as a one-time exception. Added Gemini fallback in the meantime so the pipeline kept running.
google-generativeai deprecation warning
The google-generativeai package was deprecated. Running insight.py threw a FutureWarning and the gemini-1.5-flash model returned a 404. Fix: uninstalled google-generativeai, installed google-genai, updated import and client code, switched model to gemini-2.0-flash.

Updated Folder Structure
hemlineiq/
├── venv/                  ← virtual environment (not committed to git)
├── .env                   ← API keys (FRED_API_KEY, GROQ_API_KEY, GEMINI_API_KEY, NEWS_API_KEY)
├── .gitignore
├── requirements.txt       ← added this phase
├── trends.py              ← Google Trends fetcher + Hemline Index calculator
├── economic.py            ← FRED API fetcher (sentiment, unemployment, inflation)
├── news.py                ← NewsAPI scraper + keyword extractor + sentiment scorer
├── insight.py             ← LLM briefing generator (Groq primary, Gemini fallback)
├── README.md
├── Phase1_documentation.md
└── Phase2_documentation.md

Updated Tech Stack

NewsAPI — free tier (100 req/day). Used to pull fashion headlines from the last 7 days. Keyword extraction and sentiment scoring done locally in news.py. Requires NEWS_API_KEY in .env.
Google Gemini (gemini-2.0-flash) — added as LLM fallback via the google-genai SDK. Free tier, generous limits, no aggressive rate-limit enforcement. Requires GEMINI_API_KEY in .env, obtained from aistudio.google.com.
requests — used in news.py for HTTP calls to NewsAPI.

All previously documented stack components (pytrends, fredapi, Groq, python-dotenv) remain unchanged.

Second Real Output (June 10, 2026)

Hemline Index: +1 (same slight mini lean as Phase 1)
Consumer Sentiment: 49.8/100
Unemployment: 4.3%
CPI Inflation Index: 332.4
News sentiment: neutral (0.0) — NewsAPI data unavailable this run due to network, fallback triggered

AI briefing interpretation: Correctly identified the tension between the positive hemline signal and weak consumer sentiment. Noted that consumers may be expressing optimism through fashion choices while remaining cautious economically. News block acknowledged as unavailable without crashing.

What's Next (Phase 3)

Build the FastAPI backend to serve all three data sources via HTTP endpoints
Endpoints planned: /trends, /economic, /news, /briefing (combined)
React + Recharts frontend with a timeline chart overlaying hemline index against consumer sentiment, plus the live AI briefing on the dashboard
Deploy to Hugging Face Spaces