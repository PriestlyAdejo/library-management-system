from enum import Enum, auto
class ReservationStatus(Enum):
    WAITING = 1
    PENDING = 2
    CANCELLED = 3
    COMPLETED = 4
    NO_RESERVATION = 5