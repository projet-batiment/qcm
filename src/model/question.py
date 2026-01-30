from typing import List


class Question:
    def __init__(self, enonce: str, points: int = 1):
        self.enonce = enonce
        self.points = points


class QuestionQCMultiples(Question):
    def __init__(
        self,
        enonce: str,
        points: int,
        choix_rep: List[str],
        id_bonne_reponse: List[int],
    ):
        """
        :param id_bonne_reponse: Une LISTE d'indices corrects (ex: [0] ou [0, 2])
        """
        super().__init__(enonce, points)
        self.choix_rep = choix_rep
        self.id_bonne_reponse = id_bonne_reponse
        if choix_rep is None:
            self.choix_rep = []
        else:
            self.choix_rep = choix_rep


class QuestionQCUnique(Question):
    def __init__(
        self, enonce: str, points: int, choix_rep: List[str], id_bonne_reponse: int
    ):
        """
        :param id_bonne_reponse: Un ENTIER de l'indice correct
        """
        super().__init(enonce, points)
        self.choix_rep = choix_rep
        self.id_bonne_reponse = id_bonne_reponse


class QuestionLibre(Question):
    __tablename__ = "questions_libre"
    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    rep_attendue = Column(String)
    __mapper_args__ = {"polymorphic_identity": "libre"}

    def __init__(self, enonce: str, points: int, rep_attendue: str):
        super().__init__(enonce, points)
        self.rep_attendue = rep_attendue
