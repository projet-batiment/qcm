from dataclasses import dataclass, field

from qcm.model.question import Question


@dataclass
class Qcm:
    """
    Représente un qcm, ensemble de questions.
    """

    titre: str = "Nouveau QCM"
    liste_questions: list[Question] = field(default_factory=list)

    @property
    def score(self) -> int:
        """
        Calcule le score maximal.

        Returns:
            int: score maximal
        """
        score = 0

        for i, question in enumerate(self.liste_questions):
            if not question.coherent():
                raise ValueError(f"Question #{i} is incoherent: {question}")

            score += question.points

        return score
