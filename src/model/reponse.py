class Reponse():
    def __init__(self, texte : str, est_correcte : bool = False, feedback : str =""):
        self.texte = texte
        self.est_correcte = est_correcte
        self.feedback = feedback

    def __str__(self):
        return self.texte
    
    def __repr__(self):
        return f"<Reponse(texte='{self.texte}', correct={self.est_correcte})"