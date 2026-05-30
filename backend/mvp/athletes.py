from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class Athlete(Base):
    __tablename__ = "athletes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team = Column(String)
    age = Column(Integer)
    position = Column(String)
    notes = Column(Text)