from sqlalchemy.orm import Session
from . import models

def calculate_influence_scores(db: Session):
    """
    Recalculates influence scores for all users.
    Formula:
    influence_score = (post_upvotes * 0.5) + (comment_upvotes * 0.3) + (total_mentions * 0.2)
    """
    users = db.query(models.User).all()
    for user in users:
        post_upvotes = sum(p.score for p in user.posts)
        comment_upvotes = sum(c.score for c in user.comments)
        total_mentions = len(user.posts) + len(user.comments)

        score = (post_upvotes * 0.5) + (comment_upvotes * 0.3) + (total_mentions * 0.2)
        user.influence_score = score
        
    db.commit()
