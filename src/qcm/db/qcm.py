from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from qcm.model.bdd_init import Base

if TYPE_CHECKING:
    from model.question import Question


class QcmDB(Base):
    """
    Classe modèle représentant un questionnaire (conteneur de questions).
    Elle gère la collection de questions et le calcul des scores théoriques.
    """

    __tablename__ = "qcm"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    liste_questions = relationship(
        "QuestionDB",
        order_by="QuestionDB.id",
        back_populates="qcm",
        cascade="all, delete-orphan",
    )

    def __init__(
        self, titre: str, liste_questions: Optional[List["Question"]] = None
    ) -> None:
        self.titre = titre
        # SQLAlchemy gère la liste des questions.
        if liste_questions:
            self.liste_questions = liste_questions

    def ajouter_question(self, question: "Question") -> None:
        """Ajoute une question (QCM, Unique ou Libre) au questionnaire."""
        self.liste_questions.append(question)

    def supprimer_question(self, index: int) -> None:
        """Supprime une question par son index si elle existe."""
        if 0 <= index < len(self.liste_questions):
            self.liste_questions.pop(index)

    def get_question(self, index: int) -> Optional["Question"]:
        """Retourne la question à l'index donné sans la supprimer."""
        if 0 <= index < len(self.liste_questions):
            return self.liste_questions[index]
        return None

    def get_nombre_questions(self) -> int:
        """Retourne le nombre total de questions."""
        return len(self.liste_questions)

    def calculer_score_max(self) -> int:
        """
        Calcule le score total maximum possible de ce QCM.
        """
        total = 0
        for question in self.liste_questions:
            total += question.points
        return total
