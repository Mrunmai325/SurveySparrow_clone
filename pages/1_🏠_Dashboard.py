import streamlit as st
from database import get_db

def show():
    st.title("Survey Dashboard")
    
    with st.container():
        st.header("Your Surveys")
        db = next(get_db())
        surveys = db.execute("SELECT * FROM surveys").fetchall()
        
        for survey in surveys:
            with st.expander(survey.title):
                st.write(survey.description)
                if st.button("View Results", key=survey.id):
                    st.session_state.current_survey = survey.id
                    st.switch_page("pages/3_📊_Analytics.py")
