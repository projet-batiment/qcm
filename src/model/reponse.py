from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.model.bdd_init import Base


class Reponse(Base):
    __tablename__ = "reponses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    texte = Column(String, nullable=False)
    est_correcte = Column(Boolean, default=False)
    feedback = Column(String, default="")
    question_id = Column(Integer, ForeignKey("questions_qcm.id"))
    question = relationship("QuestionQCM", back_populates="choix_rep")

    def __init__(self, texte: str, est_correcte: bool = False, feedback: str = ""):
        self.texte = texte
        self.est_correcte = est_correcte
        self.feedback = feedback

    def __str__(self) -> str:
        return self.texte

    def __repr__(self) -> str:
        return f"<Reponse(texte='{self.texte}', correct={self.est_correcte})"
