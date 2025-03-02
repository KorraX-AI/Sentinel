import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from modules.news_retrieval import fetch_news, categorize_articles
from config import NEWS_API_KEY

# Function to report a cyber crime
def report_crime():
    st.subheader("Report a Cyber Crime")
    city = st.text_input("City")
    country = st.text_input("Country")
    description = st.text_area("Description")
    category = st.selectbox("Category", ["Phishing", "Malware", "Ransomware", "Hacking", "Identity Theft", "Data Breach", "DDoS Attack", "Other"])
    
    if st.button("Submit"):
        geolocator = Nominatim(user_agent="sentinel")
        try:
            location = geolocator.geocode(f"{city}, {country}", timeout=10)
        except GeocoderUnavailable:
            location = None
        if location:
            st.success("Crime reported successfully!")
            return {"location": (location.latitude, location.longitude), "description": description, "category": category}
        else:
            st.error("Could not find the location. Please enter a valid city and country.")
    return None

# Function to visualize reported crimes on a map
def visualize_crimes(crimes):
    st.subheader("Crime Map")
    map_center = [20.5937, 78.9629]  # Center of the map (example: India)
    crime_map = folium.Map(location=map_center, zoom_start=5)
    
    heat_data = []
    for crime in crimes:
        coordinates = crime["location"]
        heat_data.append(coordinates)
        folium.Marker(location=coordinates, popup=f"{crime['description']} ({crime['category']})<br><a href='{crime['url']}' target='_blank'>Read more</a>", tooltip=crime["category"]).add_to(crime_map)
    
    HeatMap(heat_data).add_to(crime_map)
    folium_static(crime_map)

# Function to store news data in crime reporting data and check for duplicates
def store_news_data(crimes, news_articles):
    geolocator = Nominatim(user_agent="sentinel")
    for article, category in news_articles:
        location_str = article['attack_location']
        description = article['description']
        url = article['url']
        try:
            location = geolocator.geocode(location_str, timeout=10)
        except GeocoderUnavailable:
            location = None
        if not location:
            location = geolocator.geocode("New York, USA", timeout=10)  # Fallback location
        if location and not any(crime['description'] == description and crime['location'] == (location.latitude, location.longitude) for crime in crimes):
            crimes.append({
                "location": (location.latitude, location.longitude),
                "description": description,
                "category": category,
                "url": url
            })

# Main function to handle crime reporting and visualization
def main():
    crimes = [
        {"location": (28.7041, 77.1025), "description": "Phishing attack", "category": "Phishing", "url": "https://example.com/phishing-attack"},
        {"location": (34.0522, -118.2437), "description": "Malware infection", "category": "Malware", "url": "https://example.com/malware-infection"},
        {"location": (51.5074, -0.1278), "description": "Ransomware attack", "category": "Ransomware", "url": "https://example.com/ransomware-attack"},
        # Sample data
        {"location": (52.5200, 13.4050), "description": "Phishing scam", "category": "Phishing", "url": "https://example.com/phishing-scam"},
        {"location": (41.9028, 12.4964), "description": "Malware infection", "category": "Malware", "url": "https://example.com/malware-infection"},
        {"location": (34.0522, -118.2437), "description": "Ransomware attack", "category": "Ransomware", "url": "https://example.com/ransomware-attack"}
    ]
    
    # Fetch and store news data with valid locations
    news_articles = fetch_news(NEWS_API_KEY)
    categorized_articles = categorize_articles(news_articles)
    store_news_data(crimes, categorized_articles)
    
    visualize_crimes(crimes)
