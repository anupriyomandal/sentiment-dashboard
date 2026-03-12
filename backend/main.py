from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .database import engine, Base
from .routes import api
from .workers.scheduler import start_workers

# Create DB tables
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CEAT Sentiment Intelligence API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev. In production, narrow it down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    logger.info("Starting application...")
    start_workers()

@app.get("/")
def root():
    return {"message": "Welcome to the CEAT Sentiment API"}
