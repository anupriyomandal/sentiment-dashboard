import os
import praw
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, sentiment, influencer
from .database import SessionLocal

logger = logging.getLogger(__name__)

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "CEAT Sentiment Intelligence Dashboard v1.0")

try:
    if REDDIT_CLIENT_ID and REDDIT_SECRET:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    else:
        reddit = None
except Exception as e:
    logger.error(f"Failed to initialize Reddit client: {e}")
    reddit = None

TARGET_SUBREDDITS = ["CarsIndia", "Cars", "Tires", "MechanicAdvice", "IndianCars", "Cartalk"]
SEARCH_QUERIES = ["CEAT", "CEAT tyres", "CEAT tires"]

def get_or_create_user(db: Session, username: str):
    if not username:
        username = "[deleted]"
    # Try fetching existing
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        user = models.User(username=username)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            # Race condition, fetch again
            user = db.query(models.User).filter(models.User.username == username).first()
    return user

def scrape_reddit_data():
    """
    Cron job function to fetch new Reddit posts and comments related to CEAT.
    """
    if not reddit:
        logger.warning("Reddit credentials missing. Skipping scrape.")
        return

    logger.info("Starting Reddit scrape job...")
    db = SessionLocal()
    try:
        subreddits_str = "+".join(TARGET_SUBREDDITS)
        subreddit = reddit.subreddit(subreddits_str)

        for query in SEARCH_QUERIES:
            # We search the past month, limit to 50 for rate handling per query. 
            for submission in subreddit.search(query, time_filter='month', limit=50):
                author_name = submission.author.name if submission.author else "[deleted]"
                user = get_or_create_user(db, author_name)

                post_text = f"{submission.title}. {submission.selftext}"
                post_sentiment = sentiment.analyze_sentiment(post_text)

                # Existing post?
                existing_post = db.query(models.Post).filter(models.Post.id == submission.id).first()
                if not existing_post:
                    if post_sentiment == "Positive":
                        user.positive_mentions += 1
                    elif post_sentiment == "Negative":
                        user.negative_mentions += 1
                    else:
                        user.neutral_mentions += 1

                    created_dt = datetime.utcfromtimestamp(submission.created_utc)
                    new_post = models.Post(
                        id=submission.id,
                        title=submission.title,
                        text=submission.selftext,
                        subreddit=str(submission.subreddit),
                        author=user.username,
                        score=submission.score,
                        comments_count=submission.num_comments,
                        sentiment=post_sentiment,
                        created_at=created_dt,
                        url=submission.url
                    )
                    db.add(new_post)
                    db.commit()

                # Fetch top comments
                submission.comments.replace_more(limit=0)
                for top_level_comment in submission.comments[:10]:
                    c_author = top_level_comment.author.name if top_level_comment.author else "[deleted]"
                    c_user = get_or_create_user(db, c_author)

                    existing_comment = db.query(models.Comment).filter(models.Comment.id == top_level_comment.id).first()
                    if not existing_comment:
                        c_sentiment = sentiment.analyze_sentiment(top_level_comment.body)

                        if c_sentiment == "Positive":
                            c_user.positive_mentions += 1
                        elif c_sentiment == "Negative":
                            c_user.negative_mentions += 1
                        else:
                            c_user.neutral_mentions += 1

                        new_comment = models.Comment(
                            id=top_level_comment.id,
                            post_id=submission.id,
                            author=c_user.username,
                            text=top_level_comment.body,
                            score=top_level_comment.score,
                            sentiment=c_sentiment
                        )
                        db.add(new_comment)
                        db.commit()

        # Update influencers globally
        influencer.calculate_influence_scores(db)
        logger.info("Scrape job completed successfully.")
    except Exception as e:
        logger.error(f"Error during scrape: {e}")
        db.rollback()
    finally:
        db.close()
