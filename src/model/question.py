class Question(ABC):
    def __init__(self, enonce : str, points = 1):
        self.enonce = enonce
        self.points = points
    

class QuestionQCM(Question):
    def __init__(self, enonce : str, points : int, choix_rep : list, id_bonne_reponse : int):
        super().__init__(enonce, points)
        self.choix_rep = choix_rep
        self.id_bonne_reponse = id_bonne_reponse

class QuestionLibre(Question):
    def __init__(self, enonce : str, points : int, rep_attendue : str)
        super().__init__(enonce, points)
        self.rep_attendue = rep_attendue