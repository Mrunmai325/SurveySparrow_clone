import streamlit as st
from sqlalchemy.orm import Session
from database.models import Survey
from database.crud import get_db
import pyperclip

def show():
    st.title("📤 Share Your Survey")
    db = next(get_db())
    
    # Survey selection
    surveys = db.query(Survey).all()
    if not surveys:
        st.warning("No surveys available to share")
        return
    
    selected = st.selectbox(
        "Select Survey",
        surveys,
        format_func=lambda x: x.title
    )
    
    if not selected:
        return
    
    # Share options
    st.subheader("Distribution Channels")
    
    tab1, tab2, tab3 = st.tabs(["🔗 Direct Link", "📧 Email", "🖥️ Embed"])
    
    with tab1:
        survey_url = f"https://your-app.streamlit.app/take_survey?survey_id={selected.id}"
        st.code(survey_url, language="text")
        if st.button("Copy Link", key="copy_link"):
            pyperclip.copy(survey_url)
            st.success("Link copied to clipboard!")
    
    with tab2:
        with st.form("email_form"):
            emails = st.text_area("Recipient Emails (comma separated)")
            subject = st.text_input("Subject", f"Please take our survey: {selected.title}")
            message = st.text_area("Message", f"Hi,\n\nWe'd appreciate your feedback on this survey:\n{survey_url}")
            
            if st.form_submit_button("Send Emails"):
                st.success(f"Emails queued for {len(emails.split(','))} recipients")
    
    with tab3:
        embed_code = f"""
        <iframe 
            src="{survey_url}" 
            width="100%" 
            height="500px"
            frameborder="0"
        ></iframe>
        """
        st.code(embed_code, language="html")
        st.markdown("Paste this code in your website HTML")
