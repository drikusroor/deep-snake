from enum import Enum
from http.client import FORBIDDEN


class GameEntity(Enum):
    EMPTY = 0
    SNAKE_HEAD = 1
    CANDY = 2
    FORBIDDEN = 3
