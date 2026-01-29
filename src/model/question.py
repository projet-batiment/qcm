from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.model.bdd_init import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    enonce = Column(String, nullable=False)
    points = Column(Integer, default=1)
    type_question = Column(String(50))
    qcm_id = Column(Integer, ForeignKey("qcm.id"))
    qcm = relationship("Qcm", back_populates="liste_questions")

    __mapper_args__ = {
        "polymorphic_identity": "question",
        "polymorphic_on": type_question,
    }

    def __init__(self, enonce: str, points: int = 1):
        self.enonce = enonce
        self.points = points


class QuestionQCM(Question):
    __tablename__ = "questions_qcm"
    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    choix_rep = relationship("Reponse", back_populates="question", cascade="all, delete-orphan")
    id_bonne_reponse = Column(Integer, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "qcm"}

    def __init__(self, enonce: str, points: int, choix_rep: list = None, id_bonne_reponse: int = -1):
        super().__init__(enonce, points)
        self.choix_rep = choix_rep
        self.id_bonne_reponse = id_bonne_reponse
        if choix_rep is None:
            self.choix_rep = []
        else:
            self.choix_rep = choix_rep


class QuestionLibre(Question):
    __tablename__ = "questions_libre"
    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    rep_attendue = Column(String)
    __mapper_args__ = {"polymorphic_identity": "libre"}

    def __init__(self, enonce: str, points: int, rep_attendue: str):
        super().__init__(enonce, points)
        self.rep_attendue = rep_attendue
