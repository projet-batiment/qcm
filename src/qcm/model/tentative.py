from dataclasses import dataclass, field

from qcm.model.reponse import (
    Reponse,
    ReponseLibre,
    ReponseQCMultiples,
    ReponseQCUnique,
)
from qcm.model.question import (
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)
from qcm.model.qcm import Qcm

from typing import Sequence


@dataclass()
class Tentative:
    """
    Représente une tentative, formulaire de réponses à un qcm.
    """

    qcm: Qcm
    nom: str = "Nouvelle tentative"
    __liste_reponses: tuple[Reponse] = field(default_factory=tuple, init=False)

    def __post_init__(self):
        reponses: list[Reponse] = []

        for question in self.qcm.liste_questions:
            match question:
                case QuestionLibre():
                    reponse_class = ReponseLibre

                case QuestionQCUnique():
                    reponse_class = ReponseQCUnique

                case QuestionQCMultiples():
                    reponse_class = ReponseQCMultiples

                case _:
                    raise ValueError(
                        f"Unkown model question type"
                        f" {question.__class__.__name__}"
                    )

            reponses.append(reponse_class(question=question))

        self.__liste_reponses = tuple(reponses)

    @property
    def qcm(self) -> Qcm:
        return self.__qcm

    @qcm.setter
    def qcm(self, qcm: Qcm):
        if hasattr(self, "__qcm"):
            raise AttributeError("Tentative.qcm is read-only")
        self.__qcm = qcm

    @property
    def liste_reponses(self) -> Qcm:
        return self.__liste_reponses

    @liste_reponses.setter
    def liste_reponses(self, liste_reponses: Sequence[Reponse]):
        raise AttributeError("Tentative.liste_reponses is read-only")
