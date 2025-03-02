import numpy as np
import streamlit as st
import requests
from config import DEEPSEEK_API_KEY

# Function to detect anomalies in crime reports using DeepSeek NLP
def detect_anomalies(crime_reports):
    anomalies = []
    url = "https://api.deepseek.com/v1/analyze"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    
    for report in crime_reports:
        payload = {"text": report['description']}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            analysis = response.json()
            if analysis.get('anomaly_score', 0) > 0.5:  # Assuming anomaly_score is part of the response
                anomalies.append(report)
    
    return anomalies

# Function to display anomalies
def display_anomalies(anomalies):
    if anomalies:
        for anomaly in anomalies:
            st.write(f"Anomalous Report: {anomaly['description']} (Category: {anomaly['category']})")
    else:
        st.write("No anomalies detected.")

# Main function to handle anomaly detection
def main():
    st.title("Anomaly Detection")
    st.subheader("Detect Anomalies in Crime Reports")
    
    # Sample crime reports
    crime_reports = [
        {"description": "Phishing attack in New York", "category": "Phishing"},
        {"description": "Malware infection in Los Angeles", "category": "Malware"},
        {"description": "Ransomware attack in London", "category": "Ransomware"}
    ]
    
    if st.button("Detect Anomalies"):
        anomalies = detect_anomalies(crime_reports)
        display_anomalies(anomalies)

if __name__ == "__main__":
    main()
