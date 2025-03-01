import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

# Function to report a cyber crime
def report_crime():
    st.subheader("Report a Cyber Crime")
    city = st.text_input("City")
    country = st.text_input("Country")
    description = st.text_area("Description")
    category = st.selectbox("Category", ["Phishing", "Malware", "Ransomware", "Hacking", "Identity Theft", "Data Breach", "DDoS Attack", "Other"])
    
    if st.button("Submit"):
        geolocator = Nominatim(user_agent="sentinel")
        location = geolocator.geocode(f"{city}, {country}")
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
        folium.Marker(location=coordinates, popup=f"{crime['description']} ({crime['category']})", tooltip=crime["category"]).add_to(crime_map)
    
    HeatMap(heat_data).add_to(crime_map)
    folium_static(crime_map)

# Function to store news data in crime reporting data and check for duplicates
def store_news_data(crimes, news_articles):
    for article, category in news_articles:
        location = article['attack_location']
        description = article['description']
        if not any(crime['description'] == description and crime['location'] == location for crime in crimes):
            crimes.append({
                "location": location,
                "description": description,
                "category": category
            })

# Main function to handle crime reporting and visualization
def main():
    crimes = [
        {"location": (28.7041, 77.1025), "description": "Phishing attack", "category": "Phishing"},
        {"location": (34.0522, -118.2437), "description": "Malware infection", "category": "Malware"},
        {"location": (51.5074, -0.1278), "description": "Ransomware attack", "category": "Ransomware"},
        # Sample data
        {"location": (40.7128, -74.0060), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (48.8566, 2.3522), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (35.6895, 139.6917), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (55.7558, 37.6173), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (39.9042, 116.4074), "description": "Phishing scam", "category": "Phishing"},
        {"location": (19.0760, 72.8777), "description": "Malware infection", "category": "Malware"},
        {"location": (37.7749, -122.4194), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (52.5200, 13.4050), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (41.9028, 12.4964), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (34.0522, -118.2437), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (40.730610, -73.935242), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (51.1657, 10.4515), "description": "Phishing scam", "category": "Phishing"},
        {"location": (35.6762, 139.6503), "description": "Malware infection", "category": "Malware"},
        {"location": (55.7558, 37.6173), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (48.8566, 2.3522), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (40.7128, -74.0060), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (19.0760, 72.8777), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (37.7749, -122.4194), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (52.5200, 13.4050), "description": "Phishing scam", "category": "Phishing"},
        {"location": (41.9028, 12.4964), "description": "Malware infection", "category": "Malware"},
        {"location": (34.0522, -118.2437), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (40.730610, -73.935242), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (51.1657, 10.4515), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (35.6762, 139.6503), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (55.7558, 37.6173), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (48.8566, 2.3522), "description": "Phishing scam", "category": "Phishing"},
        {"location": (40.7128, -74.0060), "description": "Malware infection", "category": "Malware"},
        {"location": (19.0760, 72.8777), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (37.7749, -122.4194), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (52.5200, 13.4050), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (41.9028, 12.4964), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (34.0522, -118.2437), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (40.730610, -73.935242), "description": "Phishing scam", "category": "Phishing"},
        {"location": (51.1657, 10.4515), "description": "Malware infection", "category": "Malware"},
        {"location": (35.6762, 139.6503), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (55.7558, 37.6173), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (48.8566, 2.3522), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (40.7128, -74.0060), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (19.0760, 72.8777), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (37.7749, -122.4194), "description": "Phishing scam", "category": "Phishing"},
        {"location": (52.5200, 13.4050), "description": "Malware infection", "category": "Malware"},
        {"location": (41.9028, 12.4964), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (34.0522, -118.2437), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (40.730610, -73.935242), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (51.1657, 10.4515), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (35.6762, 139.6503), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (55.7558, 37.6173), "description": "Phishing scam", "category": "Phishing"},
        {"location": (48.8566, 2.3522), "description": "Malware infection", "category": "Malware"},
        {"location": (40.7128, -74.0060), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (19.0760, 72.8777), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (37.7749, -122.4194), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (52.5200, 13.4050), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (41.9028, 12.4964), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (34.0522, -118.2437), "description": "Phishing scam", "category": "Phishing"},
        {"location": (40.730610, -73.935242), "description": "Malware infection", "category": "Malware"},
        {"location": (51.1657, 10.4515), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (35.6762, 139.6503), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (55.7558, 37.6173), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (48.8566, 2.3522), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (40.7128, -74.0060), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (19.0760, 72.8777), "description": "Phishing scam", "category": "Phishing"},
        {"location": (37.7749, -122.4194), "description": "Malware infection", "category": "Malware"},
        {"location": (52.5200, 13.4050), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (41.9028, 12.4964), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (34.0522, -118.2437), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (40.730610, -73.935242), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (51.1657, 10.4515), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (35.6762, 139.6503), "description": "Phishing scam", "category": "Phishing"},
        {"location": (55.7558, 37.6173), "description": "Malware infection", "category": "Malware"},
        {"location": (48.8566, 2.3522), "description": "Ransomware attack", "category": "Ransomware"},
        {"location": (40.7128, -74.0060), "description": "Hacking attempt", "category": "Hacking"},
        {"location": (19.0760, 72.8777), "description": "Identity theft case", "category": "Identity Theft"},
        {"location": (37.7749, -122.4194), "description": "Data breach incident", "category": "Data Breach"},
        {"location": (52.5200, 13.4050), "description": "DDoS attack", "category": "DDoS Attack"},
        {"location": (41.9028, 12.4964), "description": "Phishing scam", "category": "Phishing"},
        {"location": (34.0522, -118.2437), "description": "Malware infection", "category": "Malware"},
        {"location": (40.730610, -73.935242), "description": "Ransomware attack", "category": "Ransomware"}
    ]
    crime = report_crime()
    if crime:
        crimes.append(crime)
    visualize_crimes(crimes)
