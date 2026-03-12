export interface SentimentSummary {
  positive_count: number;
  neutral_count: number;
  negative_count: number;
}

export interface SentimentTrend {
  date: string;
  Positive: number;
  Neutral: number;
  Negative: number;
}

export interface Post {
  id: string;
  title: string;
  subreddit: string;
  upvotes: number;
  sentiment: string;
  top_comment: string | null;
  url: string;
}

export interface Influencer {
  username: string;
  influence_score: number;
  sentiment_leaning: string;
  mentions: number;
}

export interface Suggestion {
  post_id: string;
  post_title: string;
  suggestion: string;
}
