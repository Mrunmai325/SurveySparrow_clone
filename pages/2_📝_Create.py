import streamlit as st
from database import get_db

def show():
    st.title("Create Survey")
    
    with st.form("survey_form"):
        title = st.text_input("Title*")
        description = st.text_area("Description")
        
        # Question builder
        if "questions" not in st.session_state:
            st.session_state.questions = []
            
        for i, q in enumerate(st.session_state.questions):
            st.write(f"{i+1}. {q['text']} ({q['type']})")
            
        with st.expander("Add Question"):
            q_type = st.selectbox("Type", ["Text", "Multiple Choice", "Rating"])
            q_text = st.text_input("Question Text*")
            
            options = []
            if q_type == "Multiple Choice":
                options = st.text_area("Options (one per line)").split("\n")
            
            if st.button("Add Question"):
                st.session_state.questions.append({
                    "text": q_text,
                    "type": q_type.lower().replace(" ", "_"),
                    "options": options
                })
        
        if st.form_submit_button("Save Survey"):
            db = next(get_db())
            db.execute(
                "INSERT INTO surveys (title, description) VALUES (?, ?)",
                (title, description)
            )
            db.commit()
            st.success("Survey created!")
