import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# Cache the data loading function to improve performance
@st.cache_data
def load_data():
    """Load sentiment analysis data from the database."""
    with sqlite3.connect("comments_analysis.db") as conn:
        # Get sentiment summary
        summary_query = """
        SELECT feature, sentiment_category, SUM(count) as count 
        FROM sentiment_analysis 
        GROUP BY feature, sentiment_category
        """
        summary_df = pd.read_sql_query(summary_query, conn)
        
        # Get time series data
        time_query = """
        SELECT date(timestamp) as date, sentiment_category, SUM(count) as count
        FROM sentiment_analysis
        GROUP BY date(timestamp), sentiment_category
        ORDER BY date
        """
        time_df = pd.read_sql_query(time_query, conn)
        
        # Get recent raw comments
        comments_query = """
        SELECT comment_text, timestamp, sentiment 
        FROM raw_comments
        ORDER BY timestamp DESC
        LIMIT 50
        """
        try:
            comments_df = pd.read_sql_query(comments_query, conn)
        except:
            comments_df = pd.DataFrame()
            
    return summary_df, time_df, comments_df

# Dashboard Layout
st.set_page_config(page_title="YouTube Sentiment Analysis", layout="wide")
st.title("📊 YouTube Comments Sentiment Dashboard")
st.write("Automatically updated sentiment analysis of YouTube comments")

# Load data
summary_df, time_df, comments_df = load_data()

# Sidebar controls
st.sidebar.header("Dashboard Controls")
selected_feature = st.sidebar.selectbox(
    "Select Video/Feature:", 
    summary_df["feature"].unique()
)
time_range = st.sidebar.selectbox(
    "Time Range:", 
    ["Last 7 days", "Last 30 days", "All time"],
    index=2
)

# Filter data based on selections
if not time_df.empty:
    time_df['date'] = pd.to_datetime(time_df['date'])
    if time_range == "Last 7 days":
        cutoff_date = datetime.now() - pd.Timedelta(days=7)
        time_df = time_df[time_df['date'] >= cutoff_date]
    elif time_range == "Last 30 days":
        cutoff_date = datetime.now() - pd.Timedelta(days=30)
        time_df = time_df[time_df['date'] >= cutoff_date]

# Main dashboard
if summary_df.empty:
    st.warning("No sentiment data found in the database.")
else:
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    feature_data = summary_df[summary_df["feature"] == selected_feature]
    
    with col1:
        positive = feature_data[feature_data['sentiment_category'] == 'positive']['count'].sum()
        st.metric("Positive Comments", positive)
    
    with col2:
        neutral = feature_data[feature_data['sentiment_category'] == 'neutral']['count'].sum()
        st.metric("Neutral Comments", neutral)
    
    with col3:
        negative = feature_data[feature_data['sentiment_category'] == 'negative']['count'].sum()
        st.metric("Negative Comments", negative)

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Sentiment Distribution", "Trend Over Time", "Recent Comments"])

    with tab1:
        # Pie chart using Plotly for interactivity
        fig = px.pie(
            feature_data,
            values='count',
            names='sentiment_category',
            title=f'Sentiment Distribution for {selected_feature}',
            color='sentiment_category',
            color_discrete_map={
                'positive': '#4CAF50',
                'negative': '#F44336',
                'neutral': '#2196F3'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if not time_df.empty:
            # Time series chart
            fig = px.line(
                time_df,
                x='date',
                y='count',
                color='sentiment_category',
                title='Sentiment Trend Over Time',
                color_discrete_map={
                    'positive': '#4CAF50',
                    'negative': '#F44336',
                    'neutral': '#2196F3'
                },
                labels={'count': 'Number of Comments', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No time series data available")

    with tab3:
        if not comments_df.empty:
            st.dataframe(
                comments_df,
                column_config={
                    "timestamp": "Time",
                    "comment_text": "Comment",
                    "sentiment": "Sentiment"
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("No recent comments data available")

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.experimental_rerun()

# Add footer
st.markdown("---")
st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
