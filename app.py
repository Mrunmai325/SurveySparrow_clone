import streamlit as st
from streamlit_lottie import st_lottie
import json
import database.models as models
from database.crud import init_db
from sqlalchemy import create_engine

# Initialize database
engine = create_engine("sqlite:///survey.db")
init_db(engine)

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css")

# Lottie animations
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Page config
st.set_page_config(
    page_title="SurveySparrow Clone",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Create Survey", "Analytics", "Share Survey"],
    index=0
)

# Page routing
if page == "Dashboard":
    from pages import 1_🏠_Dashboard
    st.session_state.current_page = "dashboard"
    pages.1_🏠_Dashboard.show()
elif page == "Create Survey":
    from pages import 2_📝_Create_Survey
    st.session_state.current_page = "create"
    pages.2_📝_Create_Survey.show()
elif page == "Analytics":
    from pages import 3_📊_Analytics
    st.session_state.current_page = "analyze"
    pages.3_📊_Analytics.show()
elif page == "Share Survey":
    from pages import 4_📤_Share_Survey
    st.session_state.current_page = "share"
    pages.4_📤_Share_Survey.show()
