from enum import Enum, auto


class AppState(Enum):
    """
    Représente l'état de la vue (GUI)
    """
    SPLASH_SCREEN = auto()      # page d'accueil
    EDIT = auto()               # mode édition de qcm
    ANSWER = auto()             # mode édition de tentative
    CORRECTION = auto()         # mode résultats d'une tentative
