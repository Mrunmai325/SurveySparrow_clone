import streamlit as st
import pandas as pd
from database import get_db

def show():
    st.title("Survey Analytics")
    
    db = next(get_db())
    survey_id = st.session_state.get("current_survey", 1)
    
    # Response metrics
    responses = db.execute(
        "SELECT COUNT(*) FROM responses WHERE survey_id = ?",
        (survey_id,)
    ).fetchone()[0]
    
    st.metric("Total Responses", responses)
    
    # Question-wise breakdown
    questions = db.execute(
        "SELECT * FROM questions WHERE survey_id = ?",
        (survey_id,)
    ).fetchall()
    
    for q in questions:
        with st.expander(q.text):
            answers = db.execute(
                "SELECT answer_value FROM answers WHERE question_id = ?",
                (q.id,)
            ).fetchall()
            
            if q.type == "multiple_choice":
                counts = pd.Series([a[0] for a in answers]).value_counts()
                st.bar_chart(counts)
            else:
                st.write(answers)
