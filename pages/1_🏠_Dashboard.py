import streamlit as st
from streamlit_lottie import st_lottie
import json
from sqlalchemy.orm import Session
from database.models import Survey, Response
from database.crud import get_db
from datetime import datetime, timedelta
from database import get_db

openai.api_key = st.secrets["OPENAI_API_KEY"]


def show():
    db = next(get_db())  # Get database session
    surveys = db.execute("SELECT * FROM surveys").all()
    st.write(surveys)
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
        

def show():
    st.title("Survey Dashboard")
    
    # Welcome animation
    st_lottie(load_lottie("assets/animations/welcome.json"), height=200)
    
    # Metrics cards
    db = next(get_db())
    
    total_surveys = db.query(Survey).count()
    total_responses = db.query(Response).count()
    recent_responses = db.query(Response).filter(
        Response.created_at >= datetime.now() - timedelta(days=7)
    ).count()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Surveys", total_surveys)
    col2.metric("Total Responses", total_responses)
    col3.metric("This Week", recent_responses)
    
    # Recent surveys
    st.subheader("Your Surveys")
    surveys = db.query(Survey).order_by(Survey.created_at.desc()).limit(5).all()
    
    for survey in surveys:
        response_count = db.query(Response).filter_by(survey_id=survey.id).count()
        
        with st.container(border=True):
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.markdown(f"### {survey.title}")
                st.caption(survey.description)
            with col2:
                st.metric("Responses", response_count)
                st.button(
                    "Analyze →", 
                    key=f"analyze_{survey.id}",
                    on_click=lambda: st.session_state.update({"selected_survey": survey.id})
                )
    
    # Quick actions
    st.subheader("Quick Actions")
    st.button("🚀 Create New Survey", use_container_width=True)
    st.button("📤 Share Existing Survey", use_container_width=True)
