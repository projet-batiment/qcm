class Qcm:
    def __init__(self, titre: str, liste_questions=None):
        self.titre = titre
        if liste_questions is None:
            self.liste_questions = []
        else:
            self.liste_questions = liste_questions
