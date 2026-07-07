from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base

class ResearchCard(Base):
    __tablename__ = "research_cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    doi = Column(String, unique=True, index=True)
    summary=Column(Text)
    objective=Column(Text)
    hypothesis=Column(Text)
    methods=Column(Text)
    dataset=Column(Text)
    conclusion=Column(Text)
    research_gap=Column(Text)
    keywords=Column(Text)