import os
import logging
from transformers import pipeline
import openai

logger = logging.getLogger(__name__)

# Try to load HuggingFace Transformers sentiment analyzer, gracefully handling absence of large model downloads
try:
    # A standard fast model for positive/negative classification. 
    # For a specialized use-case involving 'Neutral', we map borderline scores or use a model that supports 3 labels.
    # distilbert-base-uncased-finetuned-sst-2-english outputs POSITIVE/NEGATIVE.
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    logger.info("Loaded Transformer Sentiment Pipeline")
except Exception as e:
    sentiment_pipeline = None
    logger.warning(f"Failed to load transformers pipeline: {e}. Falling back to keyword analysis.")

def analyze_sentiment(text: str) -> str:
    """
    Classifies the text into Positive, Neutral, or Negative sentiment.
    Specifically regarding CEAT tyres.
    """
    if not text or not text.strip():
        return "Neutral"
    
    # Simple fallback using keywords if pipeline fails
    if not sentiment_pipeline:
        lower_text = text.lower()
        positive_keywords = ["good", "great", "best", "awesome", "excellent", "durable", "love", "reliable"]
        negative_keywords = ["bad", "worst", "terrible", "awful", "puncture", "blowout", "hate", "issue"]
        
        pos_count = sum(1 for p in positive_keywords if p in lower_text)
        neg_count = sum(1 for n in negative_keywords if n in lower_text)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        return "Neutral"

    try:
        # Prevent length errors using text[:512] 
        result = sentiment_pipeline(text[:512])[0]
        label = result['label'].upper()
        score = result['score']
        
        # We synthesize 'Neutral' if the model confidence is lowish
        if score < 0.6:
            return "Neutral"
            
        if label == "POSITIVE":
            return "Positive"
        elif label == "NEGATIVE":
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        logger.error(f"Sentiment evaluation error: {e}")
        return "Neutral"

def generate_response_suggestion(post_text: str, sentiment: str) -> str:
    """
    Generates a professional brand response to negative posts using OpenAI GPT-4o-mini.
    """
    if sentiment != "Negative":
        return ""
        
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found. Using fallback response.")
        return "Thanks for sharing your experience. Could you provide the tyre model and your vehicle details so we can assist?"

    try:
        client = openai.OpenAI(api_key=api_key)
        prompt = f"""
You are a professional customer support agent for CEAT Tyres.
A user posted a negative sentiment about CEAT on Reddit. 
Draft a professional, empathetic, and concise brand response to the following post, asking for more details to assist them.

Post Context:
"{post_text}"

Response:
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful customer support representative for CEAT Tyres."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Thanks for sharing your experience. Could you provide the tyre model and your vehicle details so we can assist?"
