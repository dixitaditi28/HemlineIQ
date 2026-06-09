Phase 1: Foundation & Data Pipelines
In this initial phase, I established the core backend architecture and data-fetching pipelines for HemlineIQ. The goal was to programmatically acquire and structure the two contrasting datasets required to test George Taylor's Hemline Index: public fashion sentiment and hard macroeconomic indicators.

1. Environment & Security Setup
I initialized a Python virtual environment to isolate the project dependencies and installed the primary data-handling libraries (pandas, pytrends, fredapi). To ensure secure API authentication, particularly for the Federal Reserve data, I implemented python-dotenv to manage credentials locally via a .env file without exposing them in version control.

2. Quantifying Fashion Sentiment (trends.py)
To represent the "hemline" aspect of the theory, I built a script utilizing the unofficial Google Trends API (pytrends) to fetch 5-year historical search volumes for specific terms like "mini skirt" and "midi skirt". I implemented error handling for Google's rate limits and engineered a custom feature—the hemline_index. This metric calculates the spread between mini and midi skirt search volumes to serve as a proxy for consumer optimism versus economic caution.

3. Acquiring Macroeconomic Ground Truth (economic.py)
For the economic counterpart, I integrated the fredapi to pull live time-series data from the Federal Reserve. Using secure environment variables for authentication, this script retrieves historical data starting from 2020 for three key indicators: Consumer Sentiment (UMCSENT), the Unemployment Rate (UNRATE), and the Consumer Price Index for inflation (CPIAUCSL). These datasets are returned as a cleanly structured dictionary, setting up a reliable data pipeline for the FastAPI backend to consume in the next phase