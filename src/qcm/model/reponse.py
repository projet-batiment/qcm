from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from qcm.model.question import (
    Question,
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)


@dataclass
class Reponse(ABC):
    question: Question

    @abstractmethod
    def verifier(self) -> bool:
        pass


@dataclass
class ReponseQCUnique(Reponse):
    question: QuestionQCUnique
    reponse_choisie: int = QuestionQCUnique.NO_CHOICE_INDEX

    def verifier(self) -> bool:
        return self.question.index_bonne_reponse == self.reponse_choisie


@dataclass
class ReponseQCMultiples(Reponse):
    question: QuestionQCMultiples
    reponses_choisies: set[int] = field(default_factory=set)

    def verifier(self) -> bool:
        return self.question.index_bonnes_reponses == self.reponses_choisies


@dataclass
class ReponseLibre(Reponse):
    question: QuestionLibre
    reponse: str = "Réponse"

    def verifier(self):
        self.question.rep_attendue.strip().lower() == self.reponse.strip().lower()
