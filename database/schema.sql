CREATE TABLE IF NOT EXISTS users (
    username VARCHAR PRIMARY KEY,
    influence_score FLOAT DEFAULT 0.0,
    positive_mentions INTEGER DEFAULT 0,
    negative_mentions INTEGER DEFAULT 0,
    neutral_mentions INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    text TEXT,
    subreddit VARCHAR,
    author VARCHAR REFERENCES users(username),
    score INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    sentiment VARCHAR,
    created_at TIMESTAMP,
    url VARCHAR
);

CREATE TABLE IF NOT EXISTS comments (
    id VARCHAR PRIMARY KEY,
    post_id VARCHAR REFERENCES posts(id),
    author VARCHAR REFERENCES users(username),
    text TEXT,
    score INTEGER DEFAULT 0,
    sentiment VARCHAR
);
