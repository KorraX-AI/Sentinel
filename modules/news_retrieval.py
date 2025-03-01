import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from transformers import pipeline

# Function to fetch news articles from NewsAPI
def fetch_news(api_key, query="cybercrime", page_size=20):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    for article in articles:
        article['attack_location'] = extract_attack_location(article['description'])
    return articles

# Function to extract attack location from article description
def extract_attack_location(description):
    # Dummy implementation for extracting attack location
    # In a real scenario, use NLP techniques or a location extraction API
    if "New Delhi" in description:
        return "New Delhi, India"
    elif "Los Angeles" in description:
        return "Los Angeles, USA"
    elif "London" in description:
        return "London, UK"
    else:
        return "Unknown"

# Function to categorize articles
def categorize_articles(articles):
    categories = ["phishing", "ransomware", "malware", "hacking", "identity theft", "data breach", "DDoS attack", "other"]
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    # Dummy training data
    train_data = ["phishing attack", "ransomware attack", "malware infection", "hacking attempt", "identity theft case", "data breach incident", "DDoS attack", "other cybercrime"]
    train_labels = ["phishing", "ransomware", "malware", "hacking", "identity theft", "data breach", "DDoS attack", "other"]
    model.fit(train_data, train_labels)
    
    categorized_articles = []
    for article in articles:
        category = model.predict([article['title']])[0]
        categorized_articles.append((article, category))
    return categorized_articles

# Function to generate incident response for each article
def generate_incident_response(category):
    responses = {
        "phishing": "Notify the affected parties, change passwords, and monitor for suspicious activity.",
        "ransomware": "Isolate infected systems, restore from backups, and contact law enforcement.",
        "malware": "Run antivirus scans, remove malicious software, and update security patches.",
        "hacking": "Identify the breach, secure entry points, and conduct a thorough investigation.",
        "identity theft": "Notify affected individuals, monitor credit reports, and implement stronger authentication.",
        "data breach": "Inform affected parties, secure compromised systems, and review security policies.",
        "DDoS attack": "Mitigate the attack, scale up resources, and contact your ISP for support.",
        "other": "Assess the situation, take appropriate action, and document the incident."
    }
    return responses.get(category, "Assess the situation and take appropriate action.")

# Function to scan news for potential cyber threats
def scan_news_for_threats(api_key, query="cyber threat", page_size=20):
    articles = fetch_news(api_key, query, page_size)
    categorized_articles = categorize_articles(articles)
    return categorized_articles

# Function to display articles with incident response
def display_articles_with_response(categorized_articles):
    for article, category in categorized_articles:
        st.subheader(article['title'])
        st.write(f"Category: {category}")
        st.write(f"Attack Location: {article['attack_location']}")
        st.write(article['description'])
        st.write(f"Incident Response: {generate_incident_response(category)}")
        st.write(f"[Read more]({article['url']})")

# Main function to fetch, categorize, and display news with incident response
def main(api_key):
    articles = fetch_news(api_key)
    categorized_articles = categorize_articles(articles)
    display_articles_with_response(categorized_articles)
