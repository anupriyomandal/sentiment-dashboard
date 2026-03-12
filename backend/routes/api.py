from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict

from ..database import get_db
from .. import models, sentiment

router = APIRouter()

@router.get("/sentiment-summary")
def get_sentiment_summary(db: Session = Depends(get_db)):
    """ Returns overall sentiment count from posts AND comments. """
    post_counts = db.query(models.Post.sentiment, func.count(models.Post.id)).group_by(models.Post.sentiment).all()
    comment_counts = db.query(models.Comment.sentiment, func.count(models.Comment.id)).group_by(models.Comment.sentiment).all()
    
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for s, count in post_counts:
        counts[s] += count
    for s, count in comment_counts:
        counts[s] += count
        
    return {
        "positive_count": counts.get("Positive", 0),
        "neutral_count": counts.get("Neutral", 0),
        "negative_count": counts.get("Negative", 0)
    }

@router.get("/sentiment-over-time")
def get_sentiment_over_time(db: Session = Depends(get_db)):
    """ Returns sentiment trend grouped by day for the last 30 days """
    from datetime import timedelta
    import datetime
    
    thirty_days_ago = datetime.datetime.utcnow() - timedelta(days=30)
    
    posts = db.query(models.Post.created_at, models.Post.sentiment)\
                .filter(models.Post.created_at >= thirty_days_ago).all()
                
    trends = {}
    for created_at, sent in posts:
        day_str = created_at.strftime("%Y-%m-%d") if created_at else "Unknown"
        if day_str not in trends:
            trends[day_str] = {"date": day_str, "Positive": 0, "Neutral": 0, "Negative": 0}
        trends[day_str][sent] += 1
        
    sorted_trends = [trends[k] for k in sorted(trends.keys())]
    return sorted_trends

@router.get("/top-posts")
def get_top_posts(limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.score.desc()).limit(limit).all()
    result = []
    for p in posts:
        top_comment = None
        if p.comments:
            best_c = sorted(p.comments, key=lambda c: c.score, reverse=True)[0]
            top_comment = best_c.text
            
        result.append({
            "id": p.id,
            "title": p.title,
            "subreddit": p.subreddit,
            "upvotes": p.score,
            "sentiment": p.sentiment,
            "top_comment": top_comment,
            "url": p.url
        })
    return result

@router.get("/top-influencers")
def get_top_influencers(limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.influence_score.desc()).limit(limit).all()
    result = []
    for u in users:
        total = u.positive_mentions + u.neutral_mentions + u.negative_mentions
        if total == 0:
            leaning = "Neutral"
        else:
            if u.positive_mentions > u.negative_mentions: leaning = "Positive"
            elif u.negative_mentions > u.positive_mentions: leaning = "Negative"
            else: leaning = "Neutral"
            
        result.append({
            "username": u.username,
            "influence_score": round(u.influence_score, 2),
            "sentiment_leaning": leaning,
            "mentions": total
        })
    return result

@router.get("/recent-posts")
def get_recent_posts(limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).limit(limit).all()
    return posts

@router.post("/generate-response-suggestions")
def generate_responses(db: Session = Depends(get_db)):
    """ Analyzes negative posts and generates suggestions. """
    negative_posts = db.query(models.Post).filter(models.Post.sentiment == "Negative").order_by(models.Post.created_at.desc()).limit(5).all()
    
    suggestions = []
    for p in negative_posts:
        suggestion = sentiment.generate_response_suggestion(p.text or p.title, p.sentiment)
        if suggestion:
            suggestions.append({
                "post_id": p.id,
                "post_title": p.title,
                "suggestion": suggestion
            })
    return suggestions
