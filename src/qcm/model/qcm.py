from dataclasses import dataclass, field

from qcm.model.question import Question


@dataclass
class Qcm:
    """
    Représente un qcm, ensemble de questions.
    """

    titre: str = "Nouveau QCM"
    liste_questions: list[Question] = field(default_factory=list)
