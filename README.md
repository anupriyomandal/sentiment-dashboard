# CEAT Reddit Sentiment Intelligence Dashboard

A full-stack, production-ready web application designed to automatically monitor Reddit discussions regarding CEAT tyres and cars, analyze sentiment, detect influencers, and display intelligence on a modern dashboard.

## Features
- **Automated Data Scraping:** Hourly background workers fetching data from target subreddits using PRAW.
- **Sentiment Analysis:** Classifies text positivity (Positive, Neutral, Negative) leveraging state-of-the-art pipelines.
- **Influencer Tracking:** Custom formula for quantifying impact and reach (`influence_score`).
- **Response Suggestion Agent:** Suggest contextual, professional brand replies to negative feedback.
- **Modern UI:** React, TailwindCSS, ShadCN UI, Recharts powered dashboard featuring a sleek Pantone-inspired design.

## Architecture Diagram
```
[ Reddit API ] -> (PRAW Scraper Worker)
                       |
                       v
[ Sentiment Pipeline ] -> [ PostgreSQL / SQLite ]
                                |
                                v
                          [ FastAPI backend ]
                                |
                                v
                        [ React Dashboard ]
```

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` folder: `cd backend`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set your environment variables (see below).
4. Run the server: `python -m uvicorn backend.main:app --reload`
   The backend will start on `http://localhost:8000`.

### 2. Frontend Setup
1. Navigate to the `frontend` folder: `cd frontend`
2. Install Node dependencies: `npm install`
3. Run the Vite dev server: `npm run dev`
   The frontend will be at `http://localhost:5173`.

## Environment Variables
Create a `.env` file in the `project-root` (or export these):
```
REDDIT_CLIENT_ID="..."
REDDIT_SECRET="..."
REDDIT_USER_AGENT="CEAT Sentiment Intelligence Dashboard v1"
DATABASE_URL="sqlite:///./ceat_sentiment.db"  # Use postgresql://user:pass@host/db in prod
OPENAI_API_KEY="..." # For GPT-4o-mini response suggestions
```

## Deployment Guide
**Backend (Railway)**
1. Connect your repo to Railway.
2. Railway detects FastAPI via `requirements.txt` and a `Procfile`.
3. Create a Procfile with: `web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Set your Environment Variables in Railway settings.

**Frontend (Vercel)**
1. Connect `frontend/` folder to Vercel.
2. Set Build Command: `npm run build`
3. Set Output Directory: `dist`
4. Deploy!

### How to get Reddit API Keys
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
2. Click on **"are you a developer? create an app..."** at the bottom.
3. Fill in the details:
   - **name**: `ceat-sentiment-dashboard` (or anything you prefer)
   - **App type**: Select `script`
   - **description**: Optional
   - **about url**: Optional
   - **redirect uri**: `http://localhost:8000` (can be any localhost URL since we are just scraping)
4. Click **"create app"**.
5. You will now see your credentials:
   - **REDDIT_CLIENT_ID**: The string right under your app name (e.g., `xYzA123bC...`)
   - **REDDIT_SECRET**: The string next to `secret` (e.g., `aBcdEfgH...`)

Add these to your `.env` file!
