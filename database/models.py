from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default='now()')
    theme = Column(JSON)  # {primary_color: "#4f46e5", logo_url: ""}

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    text = Column(Text, nullable=False)
    type = Column(String(20))  # text/mcq/rating/file
    options = Column(JSON)  # For MCQ: ["Option1", "Option2"]
    order = Column(Integer)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    created_at = Column(DateTime, server_default='now()')

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey('responses.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    value = Column(Text)
