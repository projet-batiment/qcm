from dataclasses import dataclass, field

from qcm.model.question import Question


@dataclass
class Qcm:
    titre: str = "Nouveau QCM"
    liste_questions: list[Question] = field(default_factory=list)
