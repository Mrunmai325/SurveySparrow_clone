import streamlit as st
from database.crud import create_survey, add_question
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json

engine = create_engine("sqlite:///survey.db")

def show():
    st.title("📝 Create Survey")
    
    with st.form("survey_form"):
        title = st.text_input("Survey Title*")
        description = st.text_area("Description")
        
        # Theme customization
        with st.expander("🎨 Branding"):
            primary_color = st.color_picker("Primary Color", "#4f46e5")
            logo = st.file_uploader("Upload Logo", type=["png", "jpg"])
        
        # Question builder
        if "questions" not in st.session_state:
            st.session_state.questions = []
            
        for i, q in enumerate(st.session_state.questions):
            st.write(f"{i+1}. {q['text']} ({q['type']})")
            
        with st.expander("➕ Add Question"):
            q_type = st.selectbox("Type", ["Text", "Multiple Choice", "Rating"])
            q_text = st.text_input("Question Text*")
            
            options = []
            if q_type == "Multiple Choice":
                options = st.text_area("Options (one per line)").split("\n")
            elif q_type == "Rating":
                options = {
                    "min": 1,
                    "max": 5,
                    "labels": ["Poor", "Average", "Good"]
                }
            
            if st.button("Add Question"):
                st.session_state.questions.append({
                    "text": q_text,
                    "type": q_type.lower().replace(" ", "_"),
                    "options": options
                })
        
        if st.form_submit_button("💾 Save Survey"):
            with Session(engine) as db:
                survey = create_survey(
                    db,
                    title=title,
                    description=description,
                    theme={"primary_color": primary_color}
                )
                
                for i, q in enumerate(st.session_state.questions):
                    add_question(
                        db,
                        survey_id=survey.id,
                        text=q["text"],
                        q_type=q["type"],
                        options=q["options"],
                        order=i+1
                    )
                
                st.success("Survey created!")
                st.session_state.questions = []
