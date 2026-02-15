from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from qcm.model.base import Base

if TYPE_CHECKING:
    from model.reponse import Reponse


class TentativeDB(Base):
    """
    Classe modèle représentant une tentative (conteneur de questions).
    Elle gère la collection de reponses.
    """

    __tablename__ = "tentative"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=False)
    liste_reponses = relationship(
        "ReponseDB",
        back_populates="tentative",
        cascade="all, delete-orphan",
    )

    qcm_id = Column(Integer, ForeignKey("qcm.id"), nullable=False)
    qcm = relationship("QcmDB", back_populates="tentative")

    def __init__(
        self, nom: str, liste_reponses: Optional[list["Reponse"]] = None
    ) -> None:
        self.nom = nom
        # SQLAlchemy gère la liste des questions.
        if liste_reponses:
            self.liste_questions = liste_reponses
