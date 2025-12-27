import streamlit as st
import utils

# Page Configuration
st.set_page_config(
    page_title="Ben's Apps",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
utils.load_css("styles.css")

# Load Data
app_config = utils.load_apps()

# Sidebar - Add New App
if st.query_params.get("admin") == "true":
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
                            meta = utils.fetch_metadata(new_url)
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
                        utils.save_apps(app_config)
                        st.success("App added!")
                        st.rerun()

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">Ben's Apps</div>
        <div class="header-subtitle">I made these things (and 100 more).</div>
    </div>
""", unsafe_allow_html=True)

# Grid Layout
if not app_config:
    st.info("No apps configured. Add one from the sidebar!")
else:
    # Filter Logic
    all_badges = sorted(list(set(app.get("badge") for app in app_config if app.get("badge"))))
    
    if all_badges:
        try:
            # Try to use st.pills (Streamlit 1.40+)
            selected_badges = st.pills("Filter by tag", options=all_badges, selection_mode="multi")
        except AttributeError:
             # Fallback for older Streamlit versions
            selected_badges = st.multiselect("Filter by tag", options=all_badges)
            
        if selected_badges:
            app_config = [app for app in app_config if app.get("badge") in selected_badges]

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
