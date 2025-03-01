import torch
import numpy as np
import streamlit as st

# Function to detect anomalies in crime reports
def detect_anomalies(crime_reports):
    # Load the pre-trained anomaly detection model
    model = torch.load('path/to/anomaly_detection_model.pth')
    
    # Extract descriptions from crime reports and convert to tensor
    data = np.array([report['description'] for report in crime_reports])
    data_tensor = torch.tensor(data)
    
    # Get predictions from the model
    predictions = model(data_tensor)
    
    # Identify anomalies based on model predictions
    anomalies = [report for report, pred in zip(crime_reports, predictions) if pred.item() > 0.5]
    return anomalies

# Function to display anomalies
def display_anomalies(anomalies):
    for anomaly in anomalies:
        st.write(f"Anomalous Report: {anomaly['description']} (Category: {anomaly['category']})")
