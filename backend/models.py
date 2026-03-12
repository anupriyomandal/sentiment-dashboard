from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    influence_score = Column(Float, default=0.0)
    positive_mentions = Column(Integer, default=0)
    negative_mentions = Column(Integer, default=0)
    neutral_mentions = Column(Integer, default=0)
    
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    text = Column(Text)
    subreddit = Column(String, index=True)
    author = Column(String, ForeignKey("users.username"))
    score = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    sentiment = Column(String, index=True)
    created_at = Column(DateTime(timezone=True))
    url = Column(String)
    
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True, index=True)
    post_id = Column(String, ForeignKey("posts.id"))
    author = Column(String, ForeignKey("users.username"))
    text = Column(Text)
    score = Column(Integer, default=0)
    sentiment = Column(String)
    
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
