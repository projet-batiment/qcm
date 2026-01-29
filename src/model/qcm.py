from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.model.bdd_init import Base

class Qcm(Base):
    __tablename__ = 'qcm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    liste_questions = relationship("Question", back_populates="qcm", cascade="all, delete-orphan")

    def __init__(self, titre: str, liste_questions: Optional[List] =None):
        self.titre=titre
        if liste_questions is None:
            self.liste_questions = []
        else:
            self.liste_questions = liste_questions
