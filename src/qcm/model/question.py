from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class Question(ABC):
    """
    Représente une question. Entité subordonnée à un Qcm.

    Attributes:
        enonce (str): énoncé de la question
        points (int): valeur de la question en points (positive)
        obligatoire (bool): si une réponse est requise à cette question
    """

    enonce: str = "Énoncé"
    points: int = 1
    obligatoire: bool = True


@dataclass
class QuestionQC(Question):
    """
    Question à choix.

    Attributes:
        choix (list[int]): liste des choix prédéfinis proposés
    """

    choix: list[str] = field(default_factory=list)

    @abstractmethod
    def swap_choix(self, index_a, index_b) -> None:
        """
        Échange la position de deux propositions de choix

        Args:
            index_a (int): position du premier élément
            index_b (int): position du second élément
        """

        pass

    @abstractmethod
    def delete_choix(self, index):
        """
        Supprime une proposition de choix

        Args:
            index (int): position de l'élément
        """

        pass


@dataclass
class QuestionQCMultiples(QuestionQC):
    """
    Question à choix multiples (plusieurs choix bons possibles).

    Attributes:
        index_bonnes_reponses (set[int]): liste les indices des
        propositions de choix correctes
    """

    index_bonnes_reponses: set[int] = field(default_factory=set)

    def set_bonne_reponse(self, index: int, value: bool):
        """
        Définit la justesse d'une proposition de choix.
        Permet la mise à jour de index_bonnes_reponses lorsque l'on
        souhaite changer une unique valeur.

        Args:
            index (int): position de l'élément
            value (bool): l'élément est une bonne réponse
        """

        if value:
            self.index_bonnes_reponses.add(index)
        else:
            self.index_bonnes_reponses.remove(index)

    def swap_choix(self, index_a: int, index_b: int):
        """
        Implémentation de méthode abstraite
        """

        est_correct_a = index_a in self.index_bonnes_reponses
        choix_a = self.choix[index_a]

        self.set_bonne_reponse(index_a, index_b in self.index_bonnes_reponses)
        self.set_bonne_reponse(index_b, est_correct_a)
        self.choix[index_a] = self.choix[index_b]
        self.choix[index_b] = choix_a

    def delete_choix(self, index: int):
        """
        Implémentation de méthode abstraite
        """

        self.choix.pop(index)
        if index in self.index_bonnes_reponses:
            self.index_bonnes_reponses.remove(index)


@dataclass
class QuestionQCUnique(QuestionQC):
    """
    Question à choix unique (1 choix uniquement).

    Attributes:
        NO_CHOIX_INDEX (ClassVar[int]): valeur équivalant à une absence de choix
        index_bonne_reponse (int): indice de la proposition de choix correcte
    """

    NO_CHOICE_INDEX: ClassVar[int] = -1

    index_bonne_reponse: int = NO_CHOICE_INDEX

    def set_bonne_reponse(self, index: Optional[int] = None):
        """
        Définit la proposition de choix correcte.
        Permet la mise à jour de index_bonne_reponse.

        Args:
            index (Optional[int]): position de l'élément, sinon "aucun"
        """

        self.index_bonne_reponse = self.NO_CHOICE_INDEX if index is None else index

    def swap_choix(self, index_a: int, index_b: int):
        """
        Implémentation de méthode abstraite
        """

        choix_a = self.choix[index_a]
        self.choix[index_a] = self.choix[index_b]
        self.choix[index_b] = choix_a

        if self.index_bonne_reponse == index_a:
            self.index_bonne_reponse = index_b
        elif self.index_bonne_reponse == index_b:
            self.index_bonne_reponse = index_a

    def delete_choix(self, index: int):
        """
        Implémentation de méthode abstraite
        """

        self.choix.pop(index)
        if self.index_bonne_reponse == index:
            self.index_bonne_reponse = self.NO_CHOICE_INDEX


@dataclass
class QuestionLibre(Question):
    """
    Question à réponse libre (champ de texte court).

    Attributes:
        rep_attendue (str): chaine de caractères décrivant la bonne réponse
    """

    rep_attendue: str = "Réponse attendue"
