from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from qcm.db.question import (
    QuestionDB,
    QuestionLibreDB,
    QuestionQCMultiplesDB,
    QuestionQCUniqueDB,
)
from qcm.db.tentative import TentativeDB
from qcm.model.base import Base


class ReponseDB(Base):
    __tablename__ = "reponses"
    id = Column(Integer, primary_key=True, autoincrement=True)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question = relationship("QuestionDB", back_populates="reponses")

    tentative_id = Column(Integer, ForeignKey("tentative.id"), nullable=False)
    tentative = relationship("TentativeDB", back_populates="liste_reponses")

    type_reponse = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "reponse",
        "polymorphic_on": type_reponse,
    }

    def __init__(self, question: QuestionDB, tentative: TentativeDB):
        self.question = question
        self.tentative = tentative


class ReponseQCMultiplesDB(ReponseDB):
    __tablename__ = "reponses_qcm"
    id = Column(Integer, ForeignKey("reponses.id"), primary_key=True)
    choix_bdd = relationship(
        "ChoixReponse",
        back_populates="reponse",
        cascade="all, delete-orphan",
    )

    choix_choix = association_proxy(
        "choix_bdd",
        "choix",
        creator=lambda choix: ChoixReponse(choix=choix),
        # proxy_factory=set
    )

    __mapper_args__ = {"polymorphic_identity": "qcm_multiple"}

    def __init__(
        self, question: QuestionQCMultiplesDB, choix: set[int], **kwargs
    ) -> None:
        self.choix_bdd = [ChoixReponse(x) for x in choix]
        super().__init__(question, **kwargs)

    @property
    def choix(self):
        return set(self.choix_choix)


class ReponseQCUniqueDB(ReponseQCMultiplesDB):
    __mapper_args__ = {"polymorphic_identity": "qcm_unique"}

    def __init__(self, question: QuestionQCUniqueDB, choix: Optional[int], **kwargs):
        super().__init__(question, set() if choix is None else {choix}, **kwargs)

    def get_choix(self) -> Optional[int]:
        return next(iter(self.choix), None)


class ReponseLibreDB(ReponseDB):
    __tablename__ = "reponses_libre"
    id = Column(Integer, ForeignKey("reponses.id"), primary_key=True)
    reponse = Column(String)
    __mapper_args__ = {"polymorphic_identity": "libre"}

    def __init__(self, question: QuestionLibreDB, reponse: str, **kwargs):
        super().__init__(question, **kwargs)
        self.reponse = reponse


class ChoixReponse(Base):
    __tablename__ = "choix_reponse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    choix = Column(Integer, nullable=False)
    reponse_id = Column(Integer, ForeignKey("reponses_qcm.id"))
    reponse = relationship("ReponseQCMultiplesDB", back_populates="choix_bdd")

    def __init__(self, choix: int):
        self.choix = choix
