import streamlit as st
from auth import login, logout
from report import report_crime
from stats import crime_statistics
from map import crime_map
from news import fetch_news

# Let's spruce up the look and feel with some custom CSS
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

# Set up a simple flag to track if someone’s logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Sidebar setup—our app’s navigation hub
st.sidebar.title("Explore Sentinel")

# If the user’s logged in, give them a warm welcome and full access
if st.session_state["logged_in"]:
    username = st.session_state.get("username", "Friend")  # Default to "Friend" if no username
    st.sidebar.subheader(f"Hey there, {username}!")

    # Logout button with a safety net to reset the session
    if st.sidebar.button("Log Out"):
        logout()
        st.session_state["logged_in"] = False
        st.sidebar.success("You’re logged out—see you soon!")

    # Let users pick what they want to do
    chosen_page = st.sidebar.radio(
        "What would you like to do?", 
        ["Report an Incident", "Check Crime Trends", "Explore the Map", "Read Crime News"]
    )

    # Guide them to the right feature based on their choice
    try:
        if chosen_page == "Report an Incident":
            report_crime()
        elif chosen_page == "Check Crime Trends":
            crime_statistics()
        elif chosen_page == "Explore the Map":
            crime_map()
        elif chosen_page == "Read Crime News":
            fetch_news()
    except Exception as e:
        st.error(f"Oops, something went wrong: {str(e)}. Try refreshing or let us know!")

# If they’re not logged in, roll out the welcome mat
else:
    st.title("Welcome to Sentinel: Your Crime Intelligence Ally")
    st.write(
        """
        **What’s Sentinel All About?**

        Crime doesn’t stand still, and neither should we. Sentinel is your go-to tool for staying ahead 
        of the curve—think real-time crime tracking, community-powered reporting, and some clever 
        analytics to spot trends. We even use blockchain to keep evidence secure. 

        Ready to make our streets safer together? Let’s dive in!
        """
    )

    # Give guests a taste of what’s inside
    guest_choice = st.sidebar.radio(
        "Take a peek at Sentinel:", 
        ["See the Crime Map", "Catch Up on News", "Sign In"]
    )

    # Handle their selection with a bit of care
    try:
        if guest_choice == "See the Crime Map":
            crime_map()
        elif guest_choice == "Catch Up on News":
            fetch_news()
        elif guest_choice == "Sign In":
            login()
    except Exception as e:
        st.error(
            f"Hmm, we hit a snag: {str(e)}. Maybe try a different option or check your connection?"
        )
