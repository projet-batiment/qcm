from enum import Enum, auto


class CallbackCommand(Enum):
    """
    Définition des différentes commandes de retour de .MainView.
    """

    MOVE_UP = auto()  # déplacer la question vers le haut
    MOVE_DOWN = auto()  # déplacer la question vers le bas
    DELETE = auto()  # supprimer la question
    DUPLICATE = auto()  # dupliquer la question
    CHANGE_TYPE = auto()  # changer le type de question
