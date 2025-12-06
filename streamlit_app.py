import streamlit as st
import json
import requests
from bs4 import BeautifulSoup
import os

# Page Configuration
st.set_page_config(
    page_title="Ben's Apps",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .header-container {
        text-align: center;
        padding: 4rem 0 3rem 0;
    }
    .header-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(to right, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    .header-subtitle {
        font-size: 1.5rem;
        color: #4b5563;
        font-weight: 500;
        letter-spacing: -0.5px;
    }

    /* Card Styles */
    a.app-card {
        display: block;
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.25rem;
        text-decoration: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        position: relative;
        overflow: hidden;
    }
    
    a.app-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #dbeafe;
    }

    /* Gradient Top Border on Hover */
    a.app-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    a.app-card:hover::before {
        opacity: 1;
    }

    /* Card Layout */
    .app-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .card-icon {
        font-size: 1.5rem;
        line-height: 1;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
        flex-grow: 1; /* Allow title to take up remaining space before badge */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .card-badge {
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        background-color: #eff6ff;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }
    
    .card-description {
        font-size: 0.875rem;
        color: #6b7280;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2; /* Limit description to 2 lines */
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
APPS_FILE = "apps.json"

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

# Load Data
app_config = load_apps()

# Sidebar - Add New App
with st.sidebar:
    st.header("Manage Apps")
    
    with st.expander("➕ Add New App", expanded=False):
        with st.form("add_app_form"):
            new_url = st.text_input("App URL", placeholder="https://...")
            
            # Simple metadata fetching trigger could be added here with session state,
            # but for simplicity in a form, we'll let the user type or it will auto-fill on save if empty.
            
            new_title = st.text_input("Title (Optional - Auto-fetch if empty)")
            new_icon = st.text_input("Icon (Emoji)", value="🚀")
            new_desc = st.text_area("Description", value="A cool new app.")
            new_badge = st.text_input("Badge (Optional)", placeholder="New")
            
            submitted = st.form_submit_button("Add App")
            
            if submitted and new_url:
                with st.spinner("Adding app..."):
                    # Auto-fill missing data
                    if not new_title:
                        meta = fetch_metadata(new_url)
                        if meta:
                            new_title = meta['title']
                        else:
                            new_title = "My App"
                    
                    new_app = {
                        "title": new_title,
                        "icon": new_icon,
                        "description": new_desc,
                        "url": new_url,
                        "badge": new_badge if new_badge else None
                    }
                    
                    app_config.append(new_app)
                    save_apps(app_config)
                    st.success("App added!")
                    st.rerun()

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">Ben's Apps</div>
        <div class="header-subtitle">I made these things!</div>
    </div>
""", unsafe_allow_html=True)

# Grid Layout
if not app_config:
    st.info("No apps configured. Add one from the sidebar!")
else:
    # Build HTML for grid layout
    html_content = '<div class="app-grid">'
    
    for app in app_config:
        badge_html = f'<div class="card-badge">{app["badge"]}</div>' if app.get('badge') else ''
        
        card_html = f"""
        <a href="{app['url']}" class="app-card" target="_blank">
            <div class="card-header">
                <div class="card-icon">{app['icon']}</div>
                <div class="card-title">{app['title']}</div>
                {badge_html}
            </div>
            <div class="card-description">
                {app['description']}
            </div>
        </a>
        """
        html_content += card_html
        
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #9ca3af; padding: 2rem; font-size: 0.8rem;'>
        © 2025 • Built with Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)
