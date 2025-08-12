import streamlit as st
from database import init_db

# Initialize DB
init_db()

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/styles.css")

# Page config
st.set_page_config(
    page_title="Survey Tool",
    layout="centered"
)

# Navigation
page = st.sidebar.radio("Go to", ["Dashboard", "Create Survey", "Analytics"])

if page == "Dashboard":
    from pages import 1_🏠_Dashboard
    pages.1_🏠_Dashboard.show()
elif page == "Create Survey":
    from pages import 2_📝_Create
    pages.2_📝_Create.show()
else:
    from pages import 3_📊_Analytics
    pages.3_📊_Analytics.show()
