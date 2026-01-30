from typing import List, Optional
from model.question import Question


class Qcm:
    """
    Classe modèle représentant un questionnaire (conteneur de questions).
    Elle gère la collection de questions et le calcul des scores théoriques.
    """

    def __init__(
        self, titre: str, liste_questions: Optional[List[Question]] = None
    ) -> None:
        """
        Initialise le QCM.
        :param titre: Le titre du questionnaire.
        :param liste_questions: Une liste optionnelle de questions déjà existantes.
        """
        self.titre = titre
        if liste_questions is None:
            self.liste_questions: List[Question] = []
        else:
            self.liste_questions = liste_questions

    def ajouter_question(self, question: Question) -> None:
        """Ajoute une question (QCM, Unique ou Libre) au questionnaire."""
        self.liste_questions.append(question)

    def supprimer_question(self, index: int) -> None:
        """Supprime une question par son index si elle existe."""
        if 0 <= index < len(self.liste_questions):
            self.liste_questions.pop(index)

    def get_question(self, index: int) -> Optional[Question]:
        """Retourne la question à l'index donné sans la supprimer."""
        if 0 <= index < len(self.liste_questions):
            return self.liste_questions[index]
        return None

    def get_nombre_questions(self) -> int:
        """Retourne le nombre total de questions."""
        return len(self.liste_questions)

    def calculer_score_max(self) -> int:
        """
        Calcule le score total maximum possible de ce QCM.
        """
        total = 0
        for question in self.liste_questions:
            total += question.points
        return total
