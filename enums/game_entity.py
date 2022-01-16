from enum import Enum
from http.client import FORBIDDEN


class GameEntity(Enum):
    FORBIDDEN = -1
    EMPTY = 0
    SNAKE_HEAD = 1
    CANDY = 2
