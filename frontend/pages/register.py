import streamlit as st

import os
import requests

API_URL = os.getenv("MEDIASSIST_API_URL", "http://127.0.0.1:8000").rstrip("/")  ## this is the url of the backend API

def register_page():
    st.title("Register for Medi Assist")

    with st.form(key="register_form"):

        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.form_submit_button("Register"):
            if register_user(firstname, lastname, username, password):  # You would define check_register based on your criteria
                st.switch_page("app.py")    # Switch to the login page after successful registration
            else:
                st.error("Invalid credentials")

    if st.button("Login"):
        st.switch_page("app.py")

def register_user(firstname, lastname, username, password):
    try:
        response = requests.post(f"{API_URL}/users/register", 
                                 json={"firstname": firstname, "lastname": lastname, "username": username, "password": password})
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Error occurred while registering: {e}")
        return False

if __name__ == "__main__":
    register_page()