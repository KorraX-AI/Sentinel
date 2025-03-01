import streamlit as st
from auth import login, logout
from report import report_crime
from stats import crime_statistics
from map import crime_map
from news import fetch_news

st.markdown("""
    <style>
    .reportview-container {
        background: #1E1E1E; /* Darker theme for readability */
        color: #EAEAEA;
    }
    .sidebar .sidebar-content {
        background: #FF3B30;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)
    
