from abc import ABC, abstractmethod
from typing import Any

from qcm.model.question import (
    Question,
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)


class ReponseDB(ABC):
    """
    Classe abstraite qui lie une logique de vérification à une Question donnée.
    """

    def __init__(self, question: Question):
        self.question = question

    @abstractmethod
    def verifier(self, proposition_utilisateur: Any) -> bool:
        """
        Vérifie la validité de la proposition utilisateur.
        proposition_utilisateur: L'index (int) ou le texte (str)
        fourni par l'utilisateur.
        """
        pass


class ReponseQCMultiplesDB(ReponseDB):
    def __init__(self, question_qcmultiples: QuestionQCMultiples):
        super().__init__(question_qcmultiples)

    def verifier(self, proposition_utilisateur: int) -> bool:
        """
        Vérifie si l'index choisi par l'utilisateur est dans la liste
        des bonnes réponses.
        On accède aux données via self.question.
        """
        qcm: QuestionQCMultiples = self.question
        return proposition_utilisateur in qcm.id_bonne_reponse


class ReponseQCUnique(ReponseDB):
    def __init__(self, question_qcunique: QuestionQCUnique):
        super().__init__(question_qcunique)

    def verifier(self, proposition_utilisateur: int):
        qcu: QuestionQCUnique = self.question
        return proposition_utilisateur == qcu.id_bonne_reponse


class ReponseLibre(ReponseDB):
    def __init__(self, question_libre: QuestionLibre):
        super().__init__(question_libre)

    def verifier(self, proposition_utilisateur: str) -> bool:
        """
        Compare la saisie avec la réponse attendue stockée dans la question.
        """
        q_libre: QuestionLibre = self.question
        return (
            proposition_utilisateur.strip().lower()
            == q_libre.rep_attendue.strip().lower()
        )
