from enum import Enum, auto

class CallbackCommand(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    DELETE = auto()
    DUPLICATE = auto()
    CHANGE_TYPE = auto()
