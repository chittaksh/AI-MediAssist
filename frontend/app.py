import streamlit as st

import os
import requests

API_URL = os.getenv("MEDIASSIST_API_URL", "http://127.0.0.1:8000").rstrip("/")  ## this is the url of the backend API
    
def login_page():
    st.title("Login to Medi Assist")

    with st.form(key="login_form"):
    
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.form_submit_button("Login"):
            user = login(username, password)
            if user:  # You would define check_login based on your criteria
                st.session_state.user = user
                st.switch_page("pages/ai.py")    # Switch to the user page after successful login
            else:
                st.error("Invalid credentials")

    if st.button("Register"):
        st.switch_page("pages/register.py")

def login(username, password):
    try: 
        response = requests.post(f"{API_URL}/users/login", json={"username": username, "password": password})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error occurred while logging in: {e}")
        return False    

if __name__ == "__main__":
    login_page()