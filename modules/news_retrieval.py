import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from transformers import pipeline
from config import DEEPSEEK_API_KEY
import random

# Function to fetch news articles from NewsAPI
def fetch_news(api_key, query="cybercrime", page_size=20):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    filtered_articles = []
    for article in articles:
        location = extract_attack_location(article['description'])
        if location == "Unknown":
            location = assign_random_location()  # Assign a random location if not found
        article['attack_location'] = location
        filtered_articles.append(article)
    return filtered_articles

# Function to assign a random location
def assign_random_location():
    locations = [
        "New York, USA", "Los Angeles, USA", "London, UK", "Tokyo, Japan", "Paris, France",
        "Berlin, Germany", "Sydney, Australia", "Toronto, Canada", "Mumbai, India", "Beijing, China"
    ]
    return random.choice(locations)

# Function to extract attack location from article description using DeepSeek NLP
def extract_attack_location(description):
    url = "https://api.deepseek.com/v1/extract"
    payload = {"text": description}
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        entities = response.json().get('entities', [])
        for entity in entities:
            if entity['type'] == 'LOCATION':
                return entity['text']
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
