from abc import ABC, abstractmethod
from question import Question


class Reponse(ABC):
    """
    Classe abstraite.
    """

    def __init__(self, question: Question):
        self.question = question

    @abstractmethod
    def verifier(self) -> bool:
        """
        Vérifie la validité.
        :param proposition_utilisateur: Utile pour la question libre (le texte saisi).
                                        Ignoré pour le QCM (car l'objet sait déjà s'il est juste).
        """
        pass
