from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.database import Base

class Practice(Base):
    __tablename__ = "practices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    team = Column(String)
    duration = Column(Integer)
    location = Column(String)
    notes = Column(Text)