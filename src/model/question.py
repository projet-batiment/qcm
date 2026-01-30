from abc import ABC, abstractmethod


class Question(ABC):
    def __init__(self, enonce: str, points: int = 1) -> None:
        self.enonce = enonce
        self.points = points

    @abstractmethod
    def verifier(self, proposition) -> bool:
        """Vérifie si la proposition donnée est correcte."""
        pass


class QuestionQCM(Question):
    def __init__(
        self, enonce: str, points: int, choix_rep: list[str], id_bonne_reponse: int
    ):
        super().__init__(enonce, points)
        self.choix_rep = choix_rep
        self.id_bonne_reponse = id_bonne_reponse

    def verifier(self, index_utilisateur: int) -> bool:
        """Compare l'index choisi avec l'index attendu."""
        return index_utilisateur == self.id_bonne_reponse


class QuestionLibre(Question):
    def __init__(self, enonce: str, points: int, rep_attendue: str):
        super().__init__(enonce, points)
        self.rep_attendue = rep_attendue

    def verifier(self, texte_utilisateur: str) -> bool:
        """Compare les chaînes de caractères (insensible à la casse)."""
        return texte_utilisateur.strip().lower() == self.rep_attendue.lower()
