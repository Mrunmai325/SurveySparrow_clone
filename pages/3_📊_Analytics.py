import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy.orm import Session
from database.models import Survey, Question, Response, Answer
from database.crud import get_db
import openai

def generate_ai_insights(survey_title, questions, responses_df):
    prompt = f"""Analyze survey results for "{survey_title}":
    
Questions:
{'\n'.join(f"{i+1}. {q.text}" for i, q in enumerate(questions))}

Sample Responses:
{responses_df.head(3).to_string()}

Provide:
1. Key themes and sentiment analysis
2. 3 actionable recommendations
3. Notable patterns in responses"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def show():
    st.title("📊 Survey Analytics")
    db = next(get_db())
    
    # Survey selection
    surveys = db.query(Survey).all()
    if not surveys:
        st.warning("No surveys available for analysis")
        return
    
    selected = st.selectbox(
        "Select Survey",
        surveys,
        format_func=lambda x: x.title
    )
    
    if not selected:
        return
    
    # Response metrics
    responses = db.query(Response).filter_by(survey_id=selected.id).count()
    questions = db.query(Question).filter_by(survey_id=selected.id).count()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Responses", responses)
    col2.metric("Questions", questions)
    
    # Response trend chart
    st.subheader("Response Trends")
    trend_data = pd.DataFrame([
        {"date": r.created_at.date(), "count": 1} 
        for r in db.query(Response).filter_by(survey_id=selected.id)
    ])
    
    if not trend_data.empty:
        trend_data = trend_data.groupby("date").count().reset_index()
        fig = px.line(trend_data, x="date", y="count", title="Daily Responses")
        st.plotly_chart(fig, use_container_width=True)
    
    # Question-level analysis
    st.subheader("Question Breakdown")
    questions = db.query(Question).filter_by(survey_id=selected.id).order_by(Question.order).all()
    
    for q in questions:
        with st.expander(f"Q{q.order}: {q.text}"):
            answers = db.query(Answer).join(Response).filter(
                Answer.question_id == q.id,
                Response.survey_id == selected.id
            ).all()
            
            if not answers:
                st.info("No responses yet")
                continue
            
            # Visualization based on question type
            if q.type == "multiple_choice":
                counts = pd.Series([a.value for a in answers]).value_counts()
                st.bar_chart(counts)
            elif q.type == "rating":
                values = pd.Series([int(a.value) for a in answers])
                st.write(f"Average rating: {values.mean():.1f}/5")
                st.bar_chart(values.value_counts().sort_index())
            elif q.type == "text":
                if st.button("Generate AI Insights", key=f"ai_{q.id}"):
                    df = pd.DataFrame([a.value for a in answers], columns=["response"])
                    insights = generate_ai_insights(selected.title, [q], df)
                    st.markdown(insights)
