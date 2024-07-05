from enum import Enum, auto

class GenericField(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.strip()

    @classmethod
    def validate(self, value):
        return True

class StrTable(Enum):
    def __new__(cls, value, strrep):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.strrep = strrep
        return obj

    def __str__(self):
        return(self.strrep)

    @classmethod
    def validate(self, value):
        for mvalue in self.__members__.values():
            if (mvalue._value_ == value):
                return True
        return False

class StrTableWDefault(StrTable):
    @classmethod
    def _missing_(self, trash):
        try:
            return self.__members__['UNKNOWN']
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

