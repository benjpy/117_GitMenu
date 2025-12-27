import streamlit as st
import json
import requests
from bs4 import BeautifulSoup
import os

APPS_FILE = "apps.json"

def load_css(file_path):
    """Load CSS from a file and inject it into the Streamlit app."""
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_apps():
    """Load apps from JSON file."""
    if not os.path.exists(APPS_FILE):
        return []
    with open(APPS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_apps(apps):
    """Save apps to JSON file."""
    with open(APPS_FILE, "w") as f:
        json.dump(apps, f, indent=4)

def fetch_metadata(url):
    """Attempt to fetch title and icon from URL."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = "New App"
        if soup.title:
            title = soup.title.string.strip()
        
        # very basic title cleanup if it contains "Streamlit"
        if "Streamlit" in title:
            title = title.replace("Streamlit", "").strip(" -|")
            
        return {
            "title": title,
            "icon": "🚀", # Default icon
            "description": "No description provided."
        }
    except Exception as e:
        return None
