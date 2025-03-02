import streamlit as st
import requests
import time
from config import VIRUSTOTAL_API_KEY, SHODAN_API_KEY

# Function to detect malware signatures using VirusTotal API
def detect_malware_signatures(file_hashes):
    results = []
    for i, file_hash in enumerate(file_hashes):
        if i > 0 and i % 4 == 0:
            time.sleep(60)  # Wait for 60 seconds to respect the rate limit
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        response = requests.get(url, headers=headers)
        result = response.json()
        results.append(result)
    return results

# Function to display malware detection results
def display_malware_detection_results(results):
    for result in results:
        st.write(f"Malware Detection Results: {result}")

# Function to detect data breaches using Shodan API
def detect_data_breaches(ip_address):
    url = f"https://api.shodan.io/shodan/host/{ip_address}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    result = response.json()
    if 'error' in result and result['error'] == 'Requires membership or higher to access':
        return {"error": "This feature requires a Shodan membership or higher to access."}
    return result

# Function to display data breach detection results
def display_data_breach_detection_results(results):
    st.write(f"Data Breach Detection Results: {results}")

# Main function to handle threat detection
def main():
    st.title("Threat Detection")

    st.subheader("Malware Detection")
    file_hashes = st.text_area("Enter file hashes (one per line)").splitlines()
    if st.button("Detect Malware"):
        malware_results = detect_malware_signatures(file_hashes)
        display_malware_detection_results(malware_results)

    st.subheader("Data Breach Detection")
    ip_address = st.text_input("Enter IP address")
    if st.button("Detect Data Breach"):
        data_breach_results = detect_data_breaches(ip_address)
        display_data_breach_detection_results(data_breach_results)
