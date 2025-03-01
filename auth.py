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
