import os
import praw
import logging
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, sentiment, influencer
from .database import SessionLocal

logger = logging.getLogger(__name__)

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "CEAT Sentiment Intelligence Dashboard v1.0")

try:
    if REDDIT_CLIENT_ID and REDDIT_SECRET and REDDIT_CLIENT_ID != "...":
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        user = models.User(username=username)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            user = db.query(models.User).filter(models.User.username == username).first()
    return user

def inject_mock_data(db: Session):
    logger.info("Injecting mock Reddit data since API keys are missing/invalid...")
    
    mock_posts = [
        {"title": "CEAT tyres are surprisingly good for the price", "subreddit": "CarsIndia", "author": "car_enthusiast99", "score": 245, "comments_count": 42},
        {"title": "My CEAT tyres wore out very quickly", "subreddit": "Tires", "author": "angry_driver", "score": 112, "comments_count": 89},
        {"title": "Thinking about buying CEAT tyres for my car", "subreddit": "Cartalk", "author": "new_driver", "score": 56, "comments_count": 12},
        {"title": "Just did a 1000km road trip on CEAT SecuraDrive. Excellent grip!", "subreddit": "CarsIndia", "author": "road_tripper", "score": 412, "comments_count": 34},
        {"title": "Had a blowout with my 3-month-old CEAT tires on the highway. Never again.", "subreddit": "MechanicAdvice", "author": "safety_first", "score": 388, "comments_count": 105},
        {"title": "What's the general opinion on CEAT vs MRF?", "subreddit": "IndianCars", "author": "curious_buyer", "score": 75, "comments_count": 60},
        {"title": "Best budget tires? Local shop recommended CEAT.", "subreddit": "Cars", "author": "budget_builder", "score": 90, "comments_count": 22},
    ]

    mock_comments = [
        {"post_idx": 0, "text": "Agreed, been using them for 2 years without issues.", "author": "happy_customer", "score": 45},
        {"post_idx": 1, "text": "Same here. Replaced mine after just 20k miles.", "author": "disappointed22", "score": 67},
        {"post_idx": 1, "text": "Did you check your alignment though?", "author": "helpful_mechanic", "score": 12},
        {"post_idx": 3, "text": "SecuraDrive is actually quite underrated.", "author": "tyre_geek", "score": 156},
        {"post_idx": 4, "text": "That's terrifying. Glad you are okay! Contact support immediately.", "author": "concerned_user", "score": 210},
    ]

    # Insert Posts
    post_ids = []
    for i, p in enumerate(mock_posts):
        post_id = f"mock_post_{i}"
        post_ids.append(post_id)
        
        # Check if already seeded to avoid duplicates on every run
        if db.query(models.Post).filter(models.Post.id == post_id).first():
            continue
            
        user = get_or_create_user(db, p["author"])
        post_sentiment = sentiment.analyze_sentiment(p["title"])
        
        if post_sentiment == "Positive":
            user.positive_mentions += 1
        elif post_sentiment == "Negative":
            user.negative_mentions += 1
        else:
            user.neutral_mentions += 1
            
        new_post = models.Post(
            id=post_id,
            title=p["title"],
            text="",
            subreddit=p["subreddit"],
            author=user.username,
            score=p["score"],
            comments_count=p["comments_count"],
            sentiment=post_sentiment,
            created_at=datetime.utcnow(),
            url=f"https://reddit.com/r/{p['subreddit']}/comments/{post_id}"
        )
        db.add(new_post)
        db.commit()

    # Insert Comments
    for i, c in enumerate(mock_comments):
        comment_id = f"mock_comment_{i}"
        if db.query(models.Comment).filter(models.Comment.id == comment_id).first():
            continue
            
        c_user = get_or_create_user(db, c["author"])
        c_sentiment = sentiment.analyze_sentiment(c["text"])
        
        if c_sentiment == "Positive":
            c_user.positive_mentions += 1
        elif c_sentiment == "Negative":
            c_user.negative_mentions += 1
        else:
            c_user.neutral_mentions += 1
            
        new_comment = models.Comment(
            id=comment_id,
            post_id=post_ids[c["post_idx"]],
            author=c_user.username,
            text=c["text"],
            score=c["score"],
            sentiment=c_sentiment
        )
        db.add(new_comment)
        db.commit()

    influencer.calculate_influence_scores(db)
    logger.info("Mock data injected successfully.")

def scrape_reddit_data():
    """
    Cron job function to fetch new Reddit posts and comments related to CEAT.
    """
    db = SessionLocal()
    try:
        if not reddit:
            inject_mock_data(db)
            return

        logger.info("Starting Reddit scrape job...")
        subreddits_str = "+".join(TARGET_SUBREDDITS)
        subreddit = reddit.subreddit(subreddits_str)

        for query in SEARCH_QUERIES:
            for submission in subreddit.search(query, time_filter='month', limit=50):
                author_name = submission.author.name if submission.author else "[deleted]"
                user = get_or_create_user(db, author_name)

                post_text = f"{submission.title}. {submission.selftext}"
                post_sentiment = sentiment.analyze_sentiment(post_text)

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

        influencer.calculate_influence_scores(db)
        logger.info("Scrape job completed successfully.")
    except Exception as e:
        logger.error(f"Error during scrape: {e}")
        db.rollback()
    finally:
        db.close()
