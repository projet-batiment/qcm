from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from qcm.model.question import (
    Question,
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)


@dataclass
class Reponse(ABC):
    """
    Représente une réponse. Entité subordonnée à une Tentative.

    Attributes:
        question (Question): question à laquelle répond cette entité,
                             et qui définit les possibilités de réponse
    """

    question: Question

    @abstractmethod
    def verifier(self) -> bool:
        """
        Vérifie si la réponse renseignée est correcte ou non.

        Returns:
            bool: est ce que la réponse est correcte.
        """

        pass


@dataclass
class ReponseQCUnique(Reponse):
    """
    Réponse à choix unique (1 choix uniquement).

    Attributes:
        question (QuestionQCUnique): attribut abstrait
        reponse_choisie (int): indice de la proposition de choix choisie
    """

    question: QuestionQCUnique
    __reponse_choisie: int = QuestionQCUnique.NO_CHOICE_INDEX

    def __init__(
        self, question: QuestionQCUnique, reponse_choisie: Optional[int] = None
    ):
        self.question = question
        self.reponse_choisie = reponse_choisie

    def verifier(self) -> bool:
        """
        Implémentation de méthode abstraite
        """

        return self.question.index_bonne_reponse == self.reponse_choisie

    @property
    def reponse_choisie(self) -> int:
        return self.__reponse_choisie

    @reponse_choisie.setter
    def reponse_choisie(self, index: Optional[int]) -> None:
        self.__reponse_choisie = (
            QuestionQCUnique.NO_CHOICE_INDEX if index is None else index
        )


@dataclass
class ReponseQCMultiples(Reponse):
    """
    Réponse à choix multiples (plusieurs choix bons possibles).

    Attributes:
        question (QuestionQCMultiples): attribut abstrait
        reponses_choisies (int): indices des propositions de choix choisies
    """

    question: QuestionQCMultiples
    reponses_choisies: set[int] = field(default_factory=set)

    def verifier(self) -> bool:
        """
        Implémentation de méthode abstraite
        """

        return self.question.index_bonnes_reponses == self.reponses_choisies


@dataclass
class ReponseLibre(Reponse):
    """
    Réponse à réponse libre (champ de texte court).

    Attributes:
        question (QuestionLibre): attribut abstrait
        reponse (str): réponse fournie
    """

    question: QuestionLibre
    reponse: str = "Réponse"

    def verifier(self) -> bool:
        """
        Implémentation de méthode abstraite
        """

        self.question.rep_attendue.strip().lower() == self.reponse.strip().lower()
