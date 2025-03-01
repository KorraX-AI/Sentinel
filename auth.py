import streamlit as st
from data import data, save_data 

def authenticate_user(username, password):
    """
    Check if the provided username and password match stored credentials.
    
    Args:
        username (str): The user's entered username.
        password (str): The user's entered password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    return username in data.get("users", {}) and data["users"][username] == password
    
def login():
    """Handles user login functionality with basic authentication."""
    st.sidebar.title("User Login")

    username = st.sidebar.text_input("Enter your username:")
    password = st.sidebar.text_input("Enter your password:", type="password")

    if st.sidebar.button("Sign In"):
        if authenticate_user(username, password):
            st.session_state["user_authenticated"] = True
            st.session_state["current_user"] = username
            st.sidebar.success(f"Welcome, {username}!")
        else:
            st.sidebar.error("Oops! Invalid username or password. Please try again.")
