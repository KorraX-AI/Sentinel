import streamlit as st
from modules.news_retrieval import main as news_main
from modules.crime_reporting import main as crime_main, store_news_data
from config import NEWS_API_KEY
from modules.news_retrieval import scan_news_for_threats, display_articles_with_response
from modules.crime_statistics import main as stats_main
from modules.anomaly_detection import detect_anomalies, display_anomalies
from modules.phishing_detection import detect_phishing_links, display_phishing_links
from modules.threat_detection import main as threat_detection_main

# Main application structure
def main():
    st.title("Sentinel: AI-Powered Crowd-Sourced Crime Intelligence Network")

    menu = ["Home", "Live Cyber Crime News", "Crime Reporting", "Threat Detection", "Crime Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    user_reported_crimes = [
        {"location": (28.7041, 77.1025), "description": "Phishing attack", "severity": "High", "category": "phishing"},
        {"location": (34.0522, -118.2437), "description": "Malware infection", "severity": "Medium", "category": "malware"},
        {"location": (51.5074, -0.1278), "description": "Ransomware attack", "severity": "High", "category": "ransomware"}
    ]

    if choice == "Home":
        st.subheader("Home")
        st.write("""
        Welcome to Sentinel, your AI-powered platform for threat detection and incident response.
        
        Sentinel is designed to help you stay informed about the latest cyber threats and incidents. 
        Our platform leverages advanced AI techniques to monitor and analyze cyber crime news, detect anomalies, 
        identify phishing links, and detect malware and data breaches. 
        
        Key Features:
        - Live Cyber Crime News: Stay updated with the latest news on cyber threats and incidents.
        - Crime Reporting: Report cyber crimes and visualize them on an interactive map.
        - Threat Detection: Detect malware and data breaches using advanced AI models.
        - Crime Statistics: View aggregated statistics of reported cyber crimes.
        
        Join us in making the digital world a safer place.
        """)
    elif choice == "Live Cyber Crime News":
        st.subheader("Live Cyber Crime News")
        news_main(NEWS_API_KEY)
    elif choice == "Crime Reporting":
        st.subheader("Crime Reporting")
        crime_main()
    elif choice == "Threat Detection":
        st.subheader("Threat Detection")
        threat_detection_main()
    elif choice == "Crime Statistics":
        st.subheader("Crime Statistics")
        stats_main(NEWS_API_KEY, user_reported_crimes)

if __name__ == '__main__':
    main()
