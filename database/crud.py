from sqlalchemy.orm import Session
from .models import Base, Survey, Question, Response, Answer

def init_db(engine):
    Base.metadata.create_all(engine)

def create_survey(db: Session, title: str, description: str, theme: dict):
    survey = Survey(title=title, description=description, theme=theme)
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey

def add_question(db: Session, survey_id: int, text: str, q_type: str, options: list, order: int):
    question = Question(
        survey_id=survey_id,
        text=text,
        type=q_type,
        options=options,
        order=order
    )
    db.add(question)
    db.commit()
    return question
