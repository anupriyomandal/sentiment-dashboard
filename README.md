# Anupriyo Mandal's Sentiments Intelligence Dashboard

A full-stack, production-ready web application designed to automatically monitor Reddit discussions regarding CEAT tyres and cars, analyze sentiment using HuggingFace models, detect brand influencers, and display actionable intelligence on a modern, interactive dashboard.

---

## 🚀 Features

- **Automated Data Scraper:** Background workers running an `apscheduler` cron job to fetch data from targeted automotive subreddits using PRAW. Gracefully falls back to injecting static mock data if Reddit API credentials aren't provided.
- **NLP Sentiment Analysis:** Utilizes a locally running HuggingFace text-classification pipeline (`distilbert-base-uncased-finetuned-sst-2-english`) to categorize post and comment text into Positive, Neutral, or Negative sentiment.
- **Influencer Tracking:** Custom algorithmic formulas to quantify user impact based on aggregate upvotes, comment volume, and historical sentiment leaning (`influence_score`).
- **Response Suggestion Agent:** Integrated with the OpenAI API (`gpt-4o-mini`) to dynamically generate professional brand replies tailored to contextually neutralize negative feedback.
- **Modern UI Architecture:** Built with React, Vite, TailwindCSS, ShadCN UI components, and Recharts, wrapped in a sleek, glassmorphism-inspired Pantone color palette (Green, Grey, Red).

---

## 📂 Exhaustive Folder Structure & File Purposes

```
sentiment-bot/
├── .env                       # Environment variables (API Keys, DB URLs)
├── README.md                  # This documentation file!
├── setup.py                   # Python package configuration for absolute imports
├── backend/                   # Python / FastAPI Backend application
│   ├── main.py                # FastAPI app entry point; initializes DB, CORS, & routers
│   ├── database.py            # SQLAlchemy engine setup and DB session factory
│   ├── models.py              # SQLAlchemy ORM models (User, Post, Comment tables)
│   ├── sentiment.py           # NLP Pipelines (HuggingFace DistilBERT) & OpenAI Agent logic
│   ├── influencer.py          # Logic to calculate and update global user influence scores
│   ├── reddit_scraper.py      # PRAW scraper logic and mock-data generation fallback
│   ├── requirements.txt       # Python dependencies list
│   ├── routes/                # FastAPI Endpoints
│   │   └── api.py             # Defines the REST API routes for frontend data retrieval
│   └── workers/               # Background Jobs
│       └── scheduler.py       # apscheduler config for running the scraper every hour
│
└── frontend/                  # React / Vite Frontend application
    ├── index.html             # Main HTML entry point for the React app
    ├── package.json           # Node.js dependencies and run scripts (npm run dev/build)
    ├── tailwind.config.js     # TailwindCSS configuration, overriding colors to CEAT palette
    ├── tsconfig.json          # TypeScript configuration rules
    ├── vite.config.ts         # Vite bundler configuration and path aliases
    ├── src/                   # Source code for React app
    │   ├── App.tsx            # Main Application Component assembling the Dashboard UI
    │   ├── index.css          # Global CSS, Tailwind directives, and Root CSS variables
    │   ├── main.tsx           # React DOM rendering entry point wrapper
    │   ├── types.ts           # TypeScript interfaces detailing the shape of API responses
    │   └── components/        # Reusable UI/UX Elements
    │       └── ui/            # ShadCN UI primitive components (Cards, Badges, Buttons)
```

---

## 🏗️ Architecture Flow Diagram

```text
[ Reddit API / Mock Data ] -> (PRAW Scraper Worker - `reddit_scraper.py`)
                                     |
                                     v
[ HuggingFace Pipeline ]  ->  [ SQLite / PostgreSQL ] <- (Influencer Calc - `influencer.py`)
   (`sentiment.py`)                  |
                                     v
[ OpenAI GPT-4o-mini ]    <-  [ FastAPI Backend ]
                                     |
                                     v
                              [ React Dashboard ]
```

---

## 💻 Setup & Execution Instructions

### 1. Environment Variables Configuration
Create a `.env` file in the root directory (`sentiment-bot/`) with the following mapping:
```env
# Required for connecting to Reddit (Leave blank to use robust mock data)
REDDIT_CLIENT_ID="..."
REDDIT_SECRET="..."
REDDIT_USER_AGENT="CEAT Sentiment Intelligence Dashboard v1"

# Required for AI response suggestions (Dashboard will skip AI calls if blank)
OPENAI_API_KEY="..." 

# Database config (Defaults to local SQLite ceat_sentiment.db if missing)
# DATABASE_URL="postgresql://user:pass@host/db"
```

### 2. Launching the Backend
Open Terminal 1:
```bash
# Navigate to project root
cd sentiment-bot

# Install python dependencies
pip install -r backend/requirements.txt

# Install backend as an editable package (resolves import errors)
pip install -e .

# Start the uvicorn development server
python3 -m uvicorn backend.main:app --reload

# The API should now be running at http://localhost:8000
```

### 3. Launching the Frontend
Open Terminal 2:
```bash
# Navigate to the frontend directory
cd frontend

# Install Node modules
npm install

# Start the Vite development server
npm run dev

# The Dashboard should now be accessible at http://localhost:5173
```

---

## 🌍 Platform Deployment Guide

### Deploying the Backend (Render / Railway)
1. Ensure your repository is pushed to GitHub.
2. Connect your repo to platforms like Railway or Render.
3. They will auto-detect the Python app via `requirements.txt`.
4. Configure the Build Command to: `pip install -e .`
5. Configure the Start Command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Add your Environment Variables (`REDDIT_CLIENT_ID`, `OPENAI_API_KEY`, etc.) in their respective settings panels.

### Deploying the Frontend (Vercel / Netlify)
1. Connect the `frontend/` folder of your repository to Vercel.
2. The framework will be correctly auto-detected as Vite.
3. Set the **Build Command:** `npm run build`
4. Set the **Output Directory:** `dist`
5. Note: Since the frontend needs to talk to the backend, you will eventually need to update the `fetch()` URLs in `App.tsx` from `http://localhost:8000` to your deployed backend URL.
6. Deploy!

---

## 🔑 How to get Reddit API Keys (Optional)
If you wish to stop using the mock dummy data and scrape live Reddit threads:
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
2. Click on **"are you a developer? create an app..."** at the bottom.
3. Fill in the Form:
   - **name**: `sentiment-dashboard`
   - **App type**: Select `script`
   - **redirect uri**: `http://localhost:8000`
4. Click **"create app"**.
5. Save the credentials displayed into your `.env` file:
   - **REDDIT_CLIENT_ID**: The 14-character string under the app name.
   - **REDDIT_SECRET**: The 27-character string next to `secret`.
