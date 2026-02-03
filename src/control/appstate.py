from enum import Enum, auto

class AppState(Enum):
    SPLASH_SCREEN = auto()
    EDIT = auto()
    ANSWER = auto()
    CORRECTION = auto()
