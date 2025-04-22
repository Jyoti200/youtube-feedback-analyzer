import nltk
import logging
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from Fetch_comments import comments  # Import comments from Fetch_comments.py

nltk.download("vader_lexicon", quiet=True)

def analyze_sentiment(comments):
    """
    Analyze sentiment of comments using VADER.
    
    Args:
        comments (list): List of comment strings.

    Returns:
        dict: Sentiment summary with counts for 'positive', 'neutral', and 'negative'.
    """
    if not comments:
        logging.warning("No comments provided for sentiment analysis.")
        return {"positive": 0, "neutral": 0, "negative": 0}

    sia = SentimentIntensityAnalyzer()
    sentiment_summary = Counter({"positive": 0, "neutral": 0, "negative": 0})

    for comment in comments:
        if not isinstance(comment, str):
            logging.warning(f"Skipping non-text comment: {comment}")
            continue

        score = sia.polarity_scores(comment)["compound"]
        if score > 0.05:
            sentiment_summary["positive"] += 1
        elif score < -0.05:
            sentiment_summary["negative"] += 1
        else:
            sentiment_summary["neutral"] += 1

    return dict(sentiment_summary)

if __name__ == "__main__":
    # Example test
    print(analyze_sentiment(comments))
