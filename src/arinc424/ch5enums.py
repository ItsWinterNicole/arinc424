from enum import Enum, auto
from math import pi

class GenericField(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.strip()

    @classmethod
    def validate(cls, value):
        return True

class FixedReal(object):
    valpos = None
    def __init__(self, value):
        if (self.valpos == None):
            self.valpos = range(0,len(value))
        num = int(value[self.valpos.start:self.valpos.stop])
        self.value = num / (10.0 * self.dplaces)

    def __float__(self):
        return self.value

    def __int__(self):
        return (round(float(self)))

    def __complex__(self):
        return (complex(float(self)))

class FixedRealDegrees(FixedReal):
    @property
    def radians(self):
        return self.value * (pi/180)

    @radians.setter
    def radians(self, value):
        self.value = value * (180/pi)

class IntentionalBlank(Enum):
    @classmethod
    def validate(cls, value):
        try:
            if (value.strip() == ''):
                return True
            return False
        except:
            return False

    @classmethod
    def _missing_(cls, value):
        return list(cls.__members__.values())[0]

    def __str__(self):
        return ''

    NONE = ''

class StrTable(Enum):
    def __new__(cls, value, strrep):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.strrep = strrep
        return obj

    def __str__(self):
        return(self.strrep)

    @classmethod
    def validate(cls, value):
        for mvalue in cls.__members__.values():
            if (mvalue._value_ == value):
                return True
        return False

class StrTableWDefault(StrTable):
    @classmethod
    def _missing_(cls, trash):
        try:
            return cls.__members__['UNKNOWN']
        except:
            raise ValueError

class RecType(StrTable):
    STANDARD = ('S', 'Standard')
    TAILORED = ('T', 'Tailored')

class AreaCodes(StrTableWDefault):
    UNITED_STATES = ('USA', "United States of America")
    AFRICA = ('AFR', "Africa")
    CANADA = ('CAN', "Canada")
    EASTER_EUR_AND_ASIA = ('EEU', "Eastern Europe and Asia")
    EUROPE = ('EUR', "Europe")
    LATIN_AMERICA = ('LAM', "Latin America")
    MIDDLE_EAST = ('MES', "Middle East")
    PACIFIC = ('PAC', "Pacific")
    SOUTH_AMERICA = ('SAM', "South America")
    SOUTH_PACIFIC = ('SPA', "South Pacific")
    UNKNOWN = (auto(), "<UNKNOWN>")

class CardinalDir(StrTable):
    @classmethod
    def _missing_(cls, val):
        for mem in cls.__members__.values():
            if mem._value_ == val.upper():
                return mem

    @property
    def lat_mul(self):
        match self._value_:
            case 'N':
                return 1
            case 'S':
                return -1

    @property
    def lon_mul(self):
        match self._value_:
            case 'E':
                return 1
            case 'W':
                return -1

    NORTH = ('N', 'North')
    SOUTH = ('S', 'South')
    EAST = ('E', 'East')
    WEST = ('W', 'West')

class DeclnCardinal(StrTable):
    @classmethod
    def _missing_(cls, val):
        for mem in cls.__members__.values():
            if mem._value_ == val.upper():
                return mem
    @property
    def multi(self):
        match self._value_:
            case 'E':
                return 1
            case 'W':
                return -1
            case 'T':
                return 0
            case 'G':
                return 0

    EAST = ('E', 'East')
    WEST = ('W', 'West')
    GRID = ('G', 'Grid')
    TRUE = ('T', 'True')
