from abc import ABC
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


@dataclass
class QuestionQCMultiples(QuestionQC):
    index_bonnes_reponses: set[int] = field(default_factory=set)

    def set_bonne_reponse(self, index: int, value: bool):
        if value:
            self.index_bonnes_reponses.add(index)
        else:
            self.index_bonnes_reponses.remove(index)


@dataclass
class QuestionQCUnique(QuestionQC):
    NO_CHOICE_INDEX: ClassVar[int] = -1

    index_bonne_reponse: int = NO_CHOICE_INDEX

    def set_bonne_reponse(self, index: Optional[int] = None):
        self.index_bonne_reponse = self.NO_CHOICE_INDEX if index is None else index


@dataclass
class QuestionLibre(Question):
    rep_attendue: str = "Réponse attendue"
