import schedule
import time
from Fetch_comments import get_comments
from analyze_comments import analyze_sentiment
from database import save_to_db

video_id = "VIDEO ID OF THE VIDEO YOU NEED TO ANALYZE"

def job():
    """Fetch, analyze, and store new comments every second."""
    print("Fetching and processing new comments...")
    comments = get_comments(video_id)
    sentiment_summary = analyze_sentiment(comments)
    save_to_db(sentiment_summary)
    print("Data saved successfully.")

# Run every second
schedule.every(10).seconds.do(job) 


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
