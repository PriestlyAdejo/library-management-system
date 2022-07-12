from enum import Enum, auto
class BookStatus(Enum):
    RESERVED = 1
    AVAILABLE = 2
    LOST = 3
    LOANED = 4
    REQUESTED = 5
