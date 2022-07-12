from enum import Enum, auto
class AccountStatus(Enum):
    ACTIVE = 1
    CLOSED = 2
    CANCELLED = 3
    BLACKLISTED = 4
    NO_ACCOUNT = 5
