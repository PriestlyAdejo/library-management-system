from enum import Enum, auto
class Race(Enum):
    # Just a note:
    """
    For enums with over 30 vals, use a text file and bring data in and convert
    to uppercase, then put underscores between words. Use the auto() method
    to automatically make the enums.
    """
    INDIAN = 1
    PAKISTANI = 2
    BANGLADESHI = 3
    CHINESE = 4
    OTHER_ASIAN = 5
    BLACK_BRITISH = 6
    CARIBBEAN = 7
    AFRICAN = 8
    OTHER_BLACK = 9
    WHITE_AND_BLACK_CARIBBEAN = 10
    WHITE_AND_BLACK_AFRICAN = 11
    WHITE_AND_BLACK_ASIAN = 12
    OTHER_MIXED = 13
    ENGLISH = 14
    WELSH = 15
    SCOTTISH = 16
    NORTHERN_IRSIH = 17
    BRITISH = 18
    IRISH = 19
    GYPSY_OR_IRISH_TRAVELLER = 20
    ROMA = 21
    OTHER_WHITE = 22
    ARAB = 23
    OTHER_ETHNIC = 24