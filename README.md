# youtube-feedback-analyzer
An interactive dashboard that analyses YouTube comments using NLP techniques to visualise public sentiment, identify feedback trends, and support data-driven decision-making.
A complete pipeline for fetching YouTube comments, analysing sentiment using VADER, and visualising results in an interactive dashboard.

## Features

- **Automated comment fetching** using YouTube API
- **Sentiment analysis** with VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **SQLite database** for persistent storage
- **Interactive dashboard** with:
  - Real-time sentiment breakdown
  - Historical trend visualisation
  - Raw comments display
- **Scheduled updates** for continuous data collection

## Install dependencies:
pip install -r requirements.txt

## 🚀 Usage
1. Fetch Comments
python fetch_comments.py --video-id YOUR_VIDEO_ID
2. Analyze Sentiment
python analyze_comments.py
3. Launch Dashboard
streamlit run dashboard.py
4. Schedule Updates 
python scheduler.py

📂 Project Structure
├── fetch_comments.py       # Fetches comments from YouTube API
├── database.py             # Database Creation and saving comments
├── comments_analysis.db    # SQLite database (auto-generated)
├── analyze_comments.py     # Performs sentiment analysis
├── dashboard.py            # Streamlit visualization
├── scheduler.py            # Automated pipeline scheduling
├── requirements.txt        # Dependencies
└── README.md               # This file

📊 Dashboard
Video in the readme file
