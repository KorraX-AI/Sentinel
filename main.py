import streamlit as st
from auth import login, logout
from report import report_crime
from stats import crime_statistics
from map import crime_map
from news import fetch_news

# Custom styling to enhance user experience
st.markdown(
    """
    <style>
    .reportview-container {
        background: #1E1E1E;  /* A dark backdrop feels sleek and easy on the eyes */
        color: #EAEAEA;       /* Light text for contrast */
    }
    .sidebar .sidebar-content {
        background: #FF3B30;  /* A bold red sidebar to grab attention */
        color: #FFFFFF;       /* White text pops nicely here */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Initialize session state if not already set
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

# Sidebar Navigation
st.sidebar.title("Navigation")

if st.session_state["user_authenticated"]:
    st.sidebar.subheader(f"Welcome, {st.session_state.get('username', 'User')}")

    if st.sidebar.button("Log Out"):
        logout()
        st.session_state["user_authenticated"] = False  # Ensure user state updates

    page_selection = st.sidebar.radio("Choose an option:", 
                                      ["Report an Incident", "Crime Trends", "Interactive Map", "Latest Crime News"])

    # Page Routing
    if page_selection == "Report an Incident":
        report_crime()
    elif page_selection == "Crime Trends":
        crime_statistics()
    elif page_selection == "Interactive Map":
        crime_map()
    elif page_selection == "Latest Crime News":
        fetch_news()

else:
    # Introduction Section
    st.title("Sentinel: AI-Powered Crime Intelligence Network")
    st.write("""
    **Project Overview:**
    
    Crime and cyber threats evolve rapidly, requiring a proactive and community-driven approach to safety. 
    Sentinel provides an intelligent, real-time crime tracking system integrating predictive analytics, 
    community reporting, and blockchain-based evidence storage.
    
    Join us in making our neighborhoods safer!
    """)

    guest_selection = st.sidebar.radio("Explore Sentinel:", ["View Crime Map", "Latest Crime News", "Sign In"])

    if guest_selection == "View Crime Map":
        crime_map()
    elif guest_selection == "Latest Crime News":
        fetch_news()
    elif guest_selection == "Sign In":
        login()
