from abc import ABC, abstractclassmethod
from dataclasses import dataclass, field
from typing import ClassVar, Optional


@dataclass
class Question(ABC):
    enonce: str = "Énoncé"
    points: int = 1
    obligatoire: bool = True


@dataclass
class QuestionQC(Question):
    choix: list[str] = field(default_factory=list)

    @abstractclassmethod
    def swap_choix(cls, index_a, index_b):
        pass

    @abstractclassmethod
    def delete_choix(cls, index):
        pass


@dataclass
class QuestionQCMultiples(QuestionQC):
    index_bonnes_reponses: set[int] = field(default_factory=set)

    def set_bonne_reponse(self, index: int, value: bool):
        if value:
            self.index_bonnes_reponses.add(index)
        else:
            self.index_bonnes_reponses.remove(index)

    def swap_choix(self, index_a: int, index_b: int):
        est_correct_a = index_a in self.index_bonnes_reponses
        choix_a = self.choix[index_a]

        self.set_bonne_reponse(index_a, index_b in self.index_bonnes_reponses)
        self.set_bonne_reponse(index_b, est_correct_a)
        self.choix[index_a] = self.choix[index_b]
        self.choix[index_b] = choix_a

    def delete_choix(self, index: int):
        self.choix.pop(index)
        if index in self.index_bonnes_reponses:
            self.index_bonnes_reponses.remove(index)


@dataclass
class QuestionQCUnique(QuestionQC):
    NO_CHOICE_INDEX: ClassVar[int] = -1

    index_bonne_reponse: int = NO_CHOICE_INDEX

    def set_bonne_reponse(self, index: Optional[int] = None):
        self.index_bonne_reponse = self.NO_CHOICE_INDEX if index is None else index

    def swap_choix(self, index_a: int, index_b: int):
        choix_a = self.choix[index_a]
        self.choix[index_a] = self.choix[index_b]
        self.choix[index_b] = choix_a

        if self.index_bonne_reponse == index_a:
            self.index_bonne_reponse = index_b
        elif self.index_bonne_reponse == index_b:
            self.index_bonne_reponse = index_a

    def delete_choix(self, index: int):
        self.choix.pop(index)
        if self.index_bonne_reponse == index:
            self.index_bonne_reponse = self.NO_CHOICE_INDEX


@dataclass
class QuestionLibre(Question):
    rep_attendue: str = "Réponse attendue"
