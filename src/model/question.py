class Question(ABC):
    def __init__(self, enonce : str, points = 1):
        self.enonce = enonce
        self.points = points