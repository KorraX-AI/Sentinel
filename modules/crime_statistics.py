import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.news_retrieval import fetch_news, categorize_articles
from modules.crime_reporting import report_crime

# Function to aggregate crime statistics
def aggregate_statistics(api_key, user_reported_crimes):
    # Fetch and categorize live news articles
    articles = fetch_news(api_key)
    categorized_articles = categorize_articles(articles)
    
    # Combine live news and user-reported crimes
    all_crimes = categorized_articles + [(crime, crime['category']) for crime in user_reported_crimes]
    
    # Aggregate statistics
    stats = {}
    for article, category in all_crimes:
        if category not in stats:
            stats[category] = 0
        stats[category] += 1
    
    return stats

# Function to display crime statistics
def display_statistics(stats):
    st.subheader("Crime Statistics")
    for category, count in stats.items():
        st.write(f"{category.capitalize()}: {count}")
    
    # Convert stats to DataFrame for visualization
    df = pd.DataFrame(list(stats.items()), columns=['Category', 'Count'])
    
    # Bar chart
    st.bar_chart(df.set_index('Category'))
    
    # Pie chart
    st.write("Pie Chart")
    fig, ax = plt.subplots()
    df.plot.pie(y='Count', labels=df['Category'], autopct='%1.1f%%', legend=False, ax=ax)
    st.pyplot(fig)

# Main function to handle crime statistics
def main(api_key, user_reported_crimes):
    stats = aggregate_statistics(api_key, user_reported_crimes)
    display_statistics(stats)
