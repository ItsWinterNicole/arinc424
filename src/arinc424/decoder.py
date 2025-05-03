from collections import defaultdict
from .ch5enums import StrTableWDefault, StrTable, GenericField, auto
from .ch5enums import CardinalDir, IntentionalBlank, DeclnCardinal, FixedReal
from .ch5enums import FixedRealDegrees
from pygeodesy.ellipsoidalExact import LatLon
from math import pi
import string

# TODO This is only returned temporarily.
class Field():
    def __init__(self, name, value, decode_fn):
        self.name = name
        self.value = value
        self.decode_fn = decode_fn

    def decode(self):
        return self.decode_fn(self.value)

class FieldOptionalBlank(Field):
    def __init__(self, name, value, decode_fn):
        if (IntentionalBlank.validate(value)):
            super().__init__(name, value, IntentionalBlank)
        else:
            super().__init__(name, value, decode_fn)

class Field_5_002(StrTable):
    STANDARD = ('S', 'Standard')
    TAILORED = ('T', 'Tailored')
    HEADER = ('H', 'Header')

# 5.3 Customer / Area Code
class Field_5_003(StrTableWDefault):
    UNKNOWN =              (auto(), '<UNKNOWN>')
    UNITED_STATES =        ('USA', 'United States of America')
    AFRICA =               ('AFR', 'Africa')
    CANADA =               ('CAN', 'Canada')
    EASTERN_EUR_AND_ASIA = ('EEU', 'Eastern Europe and Asia')
    EUROPE =               ('EUR', 'Europe')
    LATIN_AMERICA =        ('LAM', 'Latin America')
    MIDDLE_EAST =          ('MES', 'Middle East')
    PACIFIC =              ('PAC', 'Pacific')
    SOUTH_AMERICA =        ('SAM', 'Southern America')
    SOUTH_PACIFIC =        ('SPA', 'South Pacific')


# 5.4 & 5.5 Section Code & Subsection Code
class Field_5_004(StrTableWDefault):
    UNKNOWN =              (auto(), '<UNKNOWN>')
    GRID_MORA =            ('AS', 'Grid MORA')
    VHF_NAVAID =           ('D ', 'VHF Navaid')
    NDB_NAVAID =           ('DB', 'NDB Navaid')
    WAYPOINT =             ('EA', 'Waypoint')
    AIRWAYS_MARKER =       ('EM', 'Airways Marker')
    HOLDING_PATTERN =      ('EP', 'Holding Pattern')
    AIRWAYS_AND_ROUTE =    ('ER', 'Airways and Route')
    PREFERRED_ROUTE =      ('ET', 'Preferred Route')
    AIRWAY_RESTRICTIONS =  ('EU', 'Airway Restrictions')
    ENROUTE_COM =          ('EV', 'Enroute Communication')
    HELI_PADS =            ('HA', 'Heliport Pads')
    HELI_TRML_WPT =        ('HC', 'Heliport Terminal Waypoint')
    HELI_SID =             ('HD', 'Heliport SID')
    HELI_STAR =            ('HE', 'Heliport STAR')
    HELI_APCH_PROC =       ('HF', 'Heliport Approach Procedure')
    HELI_TAA =             ('HK', 'Heliport TAA')
    HELI_MSA =             ('HS', 'Heliport MSA')
    HELI_COM =             ('HV', 'Heliport Communication')
    AP_REF_POINT =         ('PA', 'Airport Reference Point')
    AP_GATES =             ('PB', 'Airport Gates')
    AP_TRML_WPT =          ('PC', 'Airport Terminal Waypoint')
    AP_SID =               ('PD', 'Airport SID')
    AP_STAR =              ('PE', 'Airport STAR')
    AP_APCH_PROC =         ('PF', 'Airport Approach Procedure')
    AP_RUNWAY =            ('PG', 'Airport Runway')
    AP_LLZ_GSLOPE =        ('PI', 'Airport Localizer/Glideslope')
    AP_TAA =               ('PK', 'Airport TAA')
    AP_MLS =               ('PL', 'Airport MLS')
    AP_LLZ_MKR =           ('PM', 'Airport Localizer Marker')
    AP_TRML_NAVAID =       ('PN', 'Airport Terminal Navaid')
    AP_PATH =              ('PP', 'Airport Path')
    AP_FLT_PLN_ARR_DEP =   ('PR', 'Airport Flt Planning ARR/DEP')
    AP_MSA =               ('PS', 'Airport MSA')
    AP_GLS_STATION =       ('PT', 'Airport GLS Station')
    AP_COM =               ('PV', 'Airport Communication')
    COMPANY_ROUTE =        ('R ', 'Company Route')
    ALTERNATE_REC =        ('RA', 'Alternate Record')
    CRUISING_TAB =         ('TC', 'Cruising Table')
    GEOG_REF =             ('TG', 'Geographical Reference')
    RNAV_NAME_TAB =        ('TN', 'RNAV Name Table')
    CTLR_AIRSPACE =        ('UC', 'Controller Airspace')
    AIRSPACE_FIR_UIR =     ('UF', 'Airspace FIR/UIR')
    RESTR_AIRSPACE =       ('UR', 'Restrictive Airspace')


# 5.6 Airport/Heliport Identifier (ARPT/HELI IDENT)
class Field_5_006(GenericField):
    # Nothing to do here.
    pass

# 5.7 Route Type
# Note: There are 5 different decoders for field_007.  (Poor spec design
#       if you ask me) but selection of the correct decoder can be done
#       at the record level, saving all the decoders from needing access
#       to the full record.
class Field_5_007ER(StrTableWDefault):
    # Enroute Airway Records (ER)
    UNKNOWN =        (auto(), 'Bad Value')
    AIRLINE_AWY =    ('A', 'Airline Airway (Tailored Data)')
    CONTROL =        ('C', 'Control')
    DCT_RTE =        ('D', 'Direct Route')
    HEL_AWYS =       ('H', 'Helicopter Airways')
    OFFC_DESG_AWYS = ('O', 'Officially Designated Airways')
    RNAV_AWYS =      ('R', 'RNAV/RNP Airways')
    UNDESG_ATS_RTE = ('S', 'Undesignated ATS Route')
    TACAN_AWY =      ('T', 'TACAN Airway')

class Field_5_007ET(StrTableWDefault):
    # Preferred Route Records (ET)
    UNKNOWN =          (auto(), 'Bad Value')
    NA_RTES =          ('C', 'North American Routes for North Atlantic Traffic Common Portion')
    PREF_RTES =        ('D', 'Preferential Routes')
    PACOTS =           ('J', 'Pacific Oceanic Transition Routes (PACOTS)')
    RNAV_AWYS =        ('M', 'RNAV Airways')
    UNDESG_ATS_RTE =   ('N', 'Undesignated ATS Route')
    PREFD_OVRFL_RTES = ('O', 'Preferred/Preferential Overflight Toutes.')
    PREFD_RTES =       ('P', 'Preferred Routes')
    TFC_OR_SYS_RTES =  ('S', 'Traffic Orientation System Routes (TOS)')
    TWR_ENRT_CTRL_RTES = ('T', 'Tower Enroute Control Routes (TEC)')

class Field_5_007_D(StrTableWDefault):
    # Preferred & Helo Route Records (PD & HD)
    UNKNOWN =             (auto(), 'Bad Value')
    ENG_OUT_SID =         ('0', 'Engine Out SID')
    SID_RWY_TRSN =        ('1', 'SID Runway Transition')
    SID_COMN_RTE =        ('2', 'SID or SID Common Route')
    SID_ENRT_TRSN =       ('3', 'SID Enroute Transition')
    RNAV_SID_RWY_TRSN =   ('4', 'RNAV SID Runway Transition')
    RNAV_SID_COMN_RTE =   ('5', 'RNAV SID or SID Common Route')
    RNAV_SID_ENRT_TRSN =  ('6', 'RNAV SID Enroute Transition')
    FMS_SID_RWY_TRSN =    ('F', 'FMS SID Runway Transition')
    FMS_SID_COMN_RTE =    ('M', 'FMS SID or SID Common Route')
    FMS_SID_ENRT_TRSN =   ('S', 'FMS SID Enroute Transition')
    VCTR_SID_RWY_TRSN =   ('T', 'Vector SID Runway Transition')
    VCTR_SID_ENRT_TRSN =  ('V', 'Vector SID Enroute Transition')

class Field_5_007_E(StrTableWDefault):
    # Airport STAR (PE) and Heliport STAR (HE) Records
    UNKNOWN =             (auto(), 'Bad Value')
    STAR_ENRT_TRSN =      ('1', 'STAR Enroute Transition')
    STAR_COMN_RTE =       ('2', 'STAR or STAR Common Route')
    STAR_RWY_TRSN =       ('3', 'STAR Runway Transition')
    RNAV_STAR_ENRT_TRSN = ('4', 'RNAV STAR Enroute Transition')
    RNAV_STAR_COMN_RTE =  ('5', 'RNAV STAR or STAR Common Route')
    RNAV_STAR_RWY_TRSN =  ('6', 'RNAV STAR Runway Transition')
    PROF_DESC_ENRT_TRSN = ('7', 'Profile Descent Enroute Transition')
    PROF_DESC_COMN_RTE =  ('8', 'Profile Descent Common Route')
    PROF_DESC_RWY_TRSN =  ('9', 'Profile Descent Runway Transition')
    FMS_STAR_ENRT_TRSN =  ('F', 'FMS STAR Enroute Transition')
    FMS_STAR_COMN_RTE =   ('M', 'FMS STAR or STAR Common Route')
    FMS_STAR_RWY_TRSN =   ('S', 'FMS STAR Runway Transition')

class Field_5_007_F(StrTableWDefault):
    # Airport STAR (PF) and Heliport STAR (HF) Records
    UNKNOWN =        (auto(), 'Bad Value')
    APCH_TRSN =      ('A', 'Approach Transition')
    LLZ_APCH =       ('B', 'Localizer/Backcourse Approach')
    VORDME_APCH =    ('D', 'VORDME Approach')
    FMS_APCH =       ('F', 'Flight Management System (FMS) Approach')
    IGS_APCH =       ('G', 'Instrument Guidance System (IGS) Approach')
    RNAV_W_RNP_PCH = ('H', 'Area Navigation (RNAV) Apch with Rqrd Nav Performance Apch')
    ILS_APCH =       ('I', 'Instrument Landing System (ILS) Approach')
    GNSS_GLS_APCH =  ('J', 'GNSS Landing System (GLS) Approach')
    LOC_APCH =       ('L', 'Localizer Only (LOC) Approach')
    MLS_APCH =       ('M', 'Microwave Landing System (MLS) Approach')
    NDB_APCH =       ('N', 'Non-Directional Beacon (NDB) Approach')
    GPS_APCH =       ('P', 'Global Position System (GPS) Approach')
    NDB_DME_APCH =   ('Q', 'Non-Directional Beacon + DME (NDB+DME) Approach')
    RNAV_APCH =      ('R', 'Area Navigation (RNAV) Approach (Note 1)')
    VORTAC_APCH =    ('S', 'VOR Approach using VORDME/VORTAC')
    TACAN_APCH =     ('T', 'TACAN Approach')
    SDF_APCH =       ('U', 'Simplified Directional Facility (SDF) Approach')
    VOR_APCH =       ('V', 'VOR Approach')
    MLSA_APCH =      ('W', 'Microwave Landing System (MLS), Type A Approach')
    LDA_APCH =       ('X', 'Localizer Directional Aid (LDA) Approach')
    MLSBC_APCH =     ('Y', 'Microwave Landing System (MLS), Type B and C Approach')
    MISSED_APCH =    ('Z', 'Missed Approach')


# 5.8 Route Identifier (ROUTE IDENT)
class Field_5_008(GenericField):
    @classmethod
    def validate(cls, value):
        # TODO Might validate length based on route type.
        # ENRT = 5 max, Prefd = 10 max
        if value.strip().isalnum():
            return True
        return False

# 5.9 SID/STAR Route Identifier (SID/STAR IDENT)
class Field_5_009(Field_5_008):
    # Same as 5.008 for now.
    # TODO Validation max = 6 char.
    pass

# 5.10 Approach Route Identifier (APPROACH IDENT)
class Field_5_010(GenericField):
    @classmethod
    def validate(cls, value):
        #TODO
        return True

    def __str__(self):
        return f"Approach: {self.value[0]}, Runway: {self.value[1:4]}"


# 5.11 Transition Identifier (TRANS IDENT)
class Field_5_011(GenericField):
    #TODO
    pass

# 5.12 Sequence Number (SEQ NR)
class Field_5_012(GenericField):
    def __str__(self):
        match len(self.value.strip()):
            case 1:
                return f'MSA Table, TAA Table, Cruise Table - Sequence No. {self.value}'
            case 2:
                return f'VHF Navaid Limitation Continuation Records - Sequence No. {self.value}'
            case 3:
                return f'SID/STAR/Approach and Company Routes - Sequence No. {self.value}'
            case 4:
                return f'Enroute Airways, Preferred Routes, FIR/UIR, and Restrictive Airspace - Sequence No. {self.value}'
            case _:
                return f'UNKNOWN SEQ NR {self.value}'


# 5.13 Fix Identifier (FIX IDENT)
class Field_5_013(GenericField):
    #TODO
    pass


# 5.14 ICAO Code (ICAO CODE)
class Field_5_014(GenericField):
    #TODO
    pass


# 5.16 Continuation Record Number (CONT NR)
class Field_5_016(GenericField):
    def __str__(self):
        match self.value:
            case '0':
                return 'Primary Record'
            case '1':
                return 'Primary Record (with Cont.)'
            case _:
                return str(self.value) + ' - Continuation'

    def __int__(self):
        # If it's an 0-9, A-Z value, base 36 should
        # cause it to convert perfectly to an int.
        # if it's something else we'll run into problems tho.
        return int(self.value, base = 36)

# 5.17 Waypoint Description Code (DESC CODE)
class Field_5_017(GenericField):
    def __str__(self):
        s = ""
        match self.value[0]:  # column 40
            case "A":
                s += "Airport as Fix"
            case "E":
                s += "Essential Waypoint"
            case "F":
                s += "Off Airway Floating Waypoint"
            case "G":
                s += "Runway/Helipad as Fix"
            case "H":
                s += "Heliport as Waypoint"
            case "N":
                s += "NDB Navaid as Waypoint"
            case "P":
                s += "Phantom Waypoint"
            case "R":
                s += "Non-Essential Waypoint"
            case "T":
                s += "Transition Essential Waypoint"
            case "V":
                s += "VHF Navaid As Fix"

        match self.value[1]:  # column 41
            case "B":
                s += "Flyover Waypoint, Ending Leg"
            case "E":
                s += "End of Continuous Segment"
            case "U":
                s += "Uncharted Airway Intersection"
            case "Y":
                s += "Fly-Over Waypoint"

        match self.value[2]:  # column 42
            case "A":
                s += "Unnamed Stepdown Fix Final Approach Segment"
            case "B":
                s += "Unnamed Stepdown Fix Intermediate Approach Segment"
            case "C":
                s += "ATC Compulsory Reporting Point"
            case "G":
                s += "Oceanic Gateway Waypoint"
            case "M":
                s += "First Leg of Missed Approach Procedure"
            case "R":
                s += "Fix used for turning final approach"
            case "S":
                s += "Named Stepdown Fix"

        match self.value[3]:  # column 43
            case "A":
                s += "Initial Approach Fix"
            case "B":
                s += "Intermediate Approach Fix"
            case "C":
                s += "Holding at Initial Approach Fix"
            case "D":
                s += "Initial Approach Fix at FACF"
            case "E":
                s += "Final End Point"
            case "F":
                s += "Final Approach Fix"
            case "G":
                s += "Source provided Enroute Waypoint without Holding"
            case "H":
                s += "Source provided Enroute Waypoint with Holding"
            case "I":
                s += "Final Approach Course Fix"
            case "M":
                s += "Missed Approach Point"
            case "N":
                s += "Engine Out SID Missed Approach Disarm Point"
            case "P":
                s += "Initial Departure Fix"
            case "Q":
                s += "Quiet Climb SID Restore Point"
        return s


# 5.18 Boundary Code (BDY CODE)
class Field_5_018(GenericField):
    def __str__(self):
        s = ""
        match self.value[0]:  # column 42
            case "U":
                s += "USA"
            case "C":
                s += "Canada"
            case "P":
                s += "Pacific"
            case "L":
                s += "Latin America"
            case "S":
                s += "South America"
            case "1":
                s += "South Pacific"
            case "E":
                s += "Europe"
            case "2":
                s += "Eastern Europe"
            case "M":
                s += "Middle East, South Asia"
            case "A":
                s += "Africa"
        return s


# 5.19 Level (LEVEL)
class Field_5_019(GenericField):
    #TODO
    pass


# 5.20 Turn Direction (TURN DIR)
class Field_5_020(GenericField):
    #TODO
    def __str__(self):
        match self.value:
            case 'R':
                return 'Right'
            case 'L':
                return 'Left'
            # TODO check this:
            case 'E':
                return 'Either'
            case ' ':
                return 'Either'
            case _:
                return 'INVALID'


# 5.21 Path and Termination (PATH TERM)
class Field_5_021(GenericField):
    #TODO
    def __str__(self):
        value = self.value.strip()
        if len(value) > 0:
            if value.isalpha() is False:
                return(f"Invalid Path and Termination: {value}")
        return value


# 5.22 Turn Direction Valid (TDV)
class Field_5_022(GenericField):
    #TODO
    def __str__(self):
        value = self.value.strip()
        if len(value) > 0:
            if value.isalpha() is False:
                return(f"Invalid Turn Direction Valid (TDV): {value}")
        return value


# 5.23 Recommended NAVAID (RECD NAV)
class Field_5_023(GenericField):
    #TODO
    def __str__(self):
        value = self.value.strip()
        if len(value) > 0:
            if value.isalnum() is False or len(value) > 4:
                return(f"Invalid Recommended NAVAID (RECD NAV): {value}")
        return value


# 5.24 Theta (THETA)
def field_024(value):
    value = value.strip()
    if len(value) > 0:
        if value.isalnum() is False or len(value) > 4:
            raise ValueError("Invalid Theta:", value)
    return value


# 5.25 Rho (RHO)
def field_025(value):
    value = value.strip()
    if len(value) > 0:
        if value.isalnum() is False or len(value) > 4:
            raise ValueError("Invalid Rho:", value)
    return value


# 5.26 Outbound Magnetic Course (OB MAG CRS)
def field_026(value):
    value = value.strip()
    if len(value) > 0:
        if value.isalnum() is False or len(value) > 4:
            raise ValueError('Invalid Outbound Magnetic Course', value)
        else:
            return "{:.1f}".format(float(value)/10)
    return value


# 5.27 Route Distance From, Holding Distance/Time (RTE DIST FROM, HOLD DIST/TIME)
class Field_5_027(GenericField):
    #TODO
    pass


# 5.28 Inbound Magnetic Course (IB MAG CRS)
class Field_5_028(GenericField):
    #TODO
    pass


# 5.29 Altitude Description (ALT DESC)
def field_029(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.30 Altitude/Minimum Altitude
def field_030(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.31 File Record Number (FRN)
class Field_5_031(GenericField):
    #TODO
    pass


# 5.32 Cycle Date (CYCLE)
def field_032(value):
    year = "19" + value[:2] if int(value[:2]) > 50 else "20" + value[:2]
    return '{}, Release {}'.format(year, value[2:])


# 5.33 VOR/NDB Identifier (VOR IDENT/NDB IDENT)
class Field_5_033(GenericField):
    #TODO
    pass


# 5.34 VOR/NDB Frequency (VOR/NDB FREQ)
def field_034(value):
    value = value.strip()
    if len(value) > 0:
        if value.isnumeric() is False:
            raise ValueError('Invalid VOR/NDB Frequency', value)
        else:
            return "{:.2f}".format(float(value)/100)
    return value


# 5.35 NAVAID class (CLASS)
class Field_5_035(GenericField):
    #TODO
    pass
    # All the commented out bits below came that way in
    # original code:
    # elif facility.contains(field):
    #     d = defaultdict(def_val)
    #     d['V'] = 'VOR'
    #     d[' '] = ''
    #     d['D'] = 'DME'
    #     d['T'] = 'TACAN'
    #     d['M'] = 'MIL TACAN'
    #     d['I'] = 'ILS/DME or ILS/TACAN'
    #     d['N'] = 'MLS/DME/N'
    #     d['P'] = 'MLS/DME/P'
    #     return ' '.join([d[val[0]], d[val[1]]]).strip()
    # elif power.contains(field):
    #     d = defaultdict(def_val)
    #     d['T'] = 'Terminal'
    #     d['L'] = 'Low Altitude'
    #     d['H'] = 'High Altitude'
    #     d['U'] = 'Undefined'
    #     d['C'] = 'ILS/TACAN'
    #     return str(d[val])
    # elif field == "Class Info":
    #     d = defaultdict(def_val)
    #     d['D'] = 'Biased ILS/DME or ILS/TACAN'
    #     d['A'] = 'Automatic Transcribed Weather Broadcast'
    #     d['B'] = 'Scheduled Weather Broadcast'
    #     d['W'] = 'No Voice on Frequency'
    #     d[' '] = 'Voice on Frequency'
    #     return str(d[val])
    # elif colloc.contains(field):
    #     collocation[' '] = 'Collocated Navaids'
    #     collocation['N'] = 'Non-Collocated Navaids'


# 5.36 Latitude (LATITUDE) & 5.37 Longitude
class Field_5_036_5_037(GenericField):
    def __init__(self, text = None, latLon = None):
        if ((text is None) and (latLon is None)):
            raise ValueError("text or geodesy arg req'd")
        if (text is None):
            self.geodesy = latLon
            return
        self.lat_card = CardinalDir(text[0])
        self.latitude = (int(text[1:3]) + (int(text[3:5]) / 60) \
                         + (float(f"{text[5:7]}.{text[7:9]}") / 60**2)) \
                         * self.lat_card.lat_mul
        self.lon_card = CardinalDir(text[9])
        self.longitude = (int(text[10:13]) + (int(text[13:15]) / 60) \
                          + (float(f"{text[15:17]}.{text[17:19]}") / 60**2)) \
                          * self.lon_card.lon_mul

    def __str__(self):
        return f"{abs(self.latitude)} {self.lat_card}, " \
               f"{abs(self.longitude)} {self.lon_card}"

    @classmethod
    def validate(cls, latlon):
        if ((latlon[0] not in ['N', 'S', 'n', 's'])
            or (latlon[9] not in ['E', 'W', 'e', 'w'])
            or (latlon[1:9].isnumeric() is not True)
            or (latlon[10:19].isnumeric() is not True)
            or (int(latlon[1:9]) > 90000000)
            or (int(latlon[3:9]) > 600000)
            or (int(latlon[5:9]) > 6000)
            or (int(latlon[10:19]) > 180000000)
            or (int(latlon[13:19]) > 600000)
            or (int(latlon[15:19]) > 6000)):
            return False
        return True

    @property
    def geodesy(self):
        """The geodesy property."""
        return LatLon(self.latitude,
                      self.longitude)

    def force_cards(self):
        # We need to force the cardinals any time
        # .latitude & .longitude are set from a source
        # outside of the arinc line strings.
        self.lat_card = CardinalDir("N")
        if (self.latitude < 0):
            self.lat_card = CardinalDir("S")
        self.lon_card = CardinalDir("E")
        if (self.longitude < 0):
            self.lon_card = CardinalDir("W")

    @geodesy.setter
    def geodesy(self, value):
        self.latitude = value.lat
        self.longitude = value.lon
        self.force_cards()

    @property
    def radians(self):
        rlat = self.latitude * (pi/180)
        rlon = self.longitude * (pi/180)
        return (rlat, rlon)

    @radians.setter
    def radians(self, value):
        self.latitude = value[0] * (180/pi)
        self.longitude = value[1] * (180/pi)
        self.force_cards()

# 5.38 DME Identifier (DME IDENT)
class Field_5_038(GenericField):
    #TODO
    pass

# 5.39 Magnetic Variation (MAG VAR, D MAG VAR)
class Field_5_039(FixedReal):
    # CWWWF is the format with WWWF being digits, and F being the
    # floating point portion of the number. C is the DeclnCardinal portion.
    dplaces = 1
    valpos = range(1,5)

    def __init__(self, value):
        if (value.strip() == ''):
            self.value = 0
            self.offset = DeclnCardinal.TRUE
        else:
            super().__init__(value) # Handle the numeric portion.
            self.offset = DeclnCardinal(value[0])
            self.value *= self.offset.multi

    def __str__(self):
        return f"{self.value:.1f} {self.offset}"

    def cardinal(self):
        return self.offset

    @property
    def radians(self):
        return self.value * (pi/180)

    @radians.setter
    def radians(self, value):
        if   (value < 0):
            self.offset = DeclnCardinal.WEST
        elif (value == 0):
            self.offset = DeclnCardinal.TRUE
        else:
            self.offset = DeclnCardinal.EAST
        self.value = value * (180/pi)

# 5.40 DME Elevation (DME ELEV)
class Field_5_040(GenericField):
    #TODO
    pass


# 5.41 Region Code (REGN CODE)
class Field_5_041(GenericField):
    #TODO
    pass


# 5.42 Waypoint Type (TYPE)
def field_042(value):
    match value[0]:
        case 'C':
            return "Combined Named Intersection and RNAV"
        case 'I':
            return 'Unnamed, Charted Intersection'
        case 'N':
            return 'NDB Navaid as Waypoint' + value[1:]
        case 'R':
            return 'Named Intersection'
        case 'U':
            return 'Uncharted Airway Intersection'
        case 'V':
            return 'VFR Waypoint'
        case 'W':
            return 'RNAV Waypoint'
    match value[1]:
        case 'A':
            return 'Final Approach Fix'
        case 'B':
            return 'Initial and Final Approach Fix'
        case 'C':
            return 'Final Approach Course Fix'
        case 'D':
            return 'Intermediate Approach Fix'
        case 'E':
            return 'Off-Route intersection in FAA National Reference System'
        case 'F':
            return 'Off-Route Intersection'
        case 'I':
            return 'Initial Approach Fix'
        case 'K':
            return 'Final Approach Course Fix at Initial Approach Fix'
        case 'L':
            return 'Final Approach Course Fix at Intermediate Approach Fix'
        case 'M':
            return 'Missed Approach Fix'
        case 'N':
            return 'Initial Approach Fix and Missed Approach Fix'
        case 'O':
            return 'Oceanic Entry/Exit Waypoint'
        case 'P':
            return 'Pitch and Catch Point in the FAA High Altitude Redesign'
        case 'S':
            return 'AACAA and SUA Waypoints in the FAA High Altitude Redesign'
        case 'U':
            return 'FIR/UIR or Controlled Airspace Intersection'
        case 'V':
            return 'Latitude/Longitude Intersection, Full Degree of Latitude'
        case 'W':
            return 'Latitude/Longitude Intersection, Half Degree of Latitude'
        case _:
            return "Unknown Waypoint Type"


# 5.43 Waypoint Name/Description (NAME/DESC)
class Field_5_043(GenericField):
    #TODO
    pass


# 5.44 Localizer/MLS/GLS Identifier (LOC, MLS, GLS IDENT)
class Field_5_044(GenericField):
    #TODO
    pass


# 5.45 Localizer Frequency (FREQ)
def field_045(value):
    if (value.isnumeric()):
        return "{:.2f}".format(float(value)/100)
    else:
        return "BAD VALUE"


# 5.46 Runway Identifier (RUNWAY ID)
class Field_5_046(GenericField):
    #TODO
    pass


# 5.47 Localizer Bearing (LOC BRG)
class Field_5_047(GenericField):
    #TODO
    pass


# 5.48 Localizer Position (LOC FR RW END Azimuth/Back Azimuth Position (AZ/BAZ FR RWEND)
class Field_5_048(GenericField):
    #TODO
    pass


# 5.49 Localizer/Azimuth Position Reference (@, +, -)
class Field_5_049(GenericField):
    #TODO
    pass


# 5.50 Glide Slope Position (GS FR RW THRES) Elevation Position (EL FR RW THRES)
class Field_5_050(GenericField):
    #TODO
    pass


# 5.51 Localizer Width (LOC WIDTH)
class Field_5_051(GenericField):
    #TODO
    pass


# 5.52 Glide Slope Angle (GS ANGLE) Minimum Elevation Angle (MIN ELEV ANGLE)
class Field_5_052(GenericField):
    #TODO
    pass


# 5.53 Transition Altitude/Level (TRANS ALTITUDE/LEVEL)
def field_053(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.54 Longest Runway (LONGEST RWY)
def field_054(value):
    if value.isnumeric():
        return value.lstrip('0')+"00" + " ft"
    else:
        return value


# 5.55 Airport/Heliport Elevation (ELEV)
class Field_5_055(GenericField):
    #TODO
    pass


# 5.56 Gate Identifier (GATE IDENT)
class Field_5_056(GenericField):
    #TODO
    pass


# 5.57 Runway Length (RUNWAY LENGTH)
class Field_5_057(GenericField):
    #TODO
    pass


# 5.58 Runway Magnetic Bearing (RWY BRG)
class Field_5_058(GenericField):
    #TODO
    pass


# 5.59 Runway Description (RUNWAY DESCRIPTION)
class Field_5_059(GenericField):
    #TODO
    pass


# 5.60 Name (NAME)
class Field_5_060(GenericField):
    #TODO
    pass


# 5.61 Notes (Continuation Records) (NOTES)
class Field_5_061(GenericField):
    #TODO
    pass


# 5.62 Inbound Holding Course (IB HOLD CRS)
class Field_5_062(GenericField):
    #TODO
    def __str__(self):
        if (self.value.isnumeric()):
            return float(self.value)/10
        else:
            return "BAD VALUE"


# 5.63 Turn (TURN)
class Field_5_063(GenericField):
    #TODO
    pass


# 5.64 Leg Length (LEG LENGTH)
class Field_5_064(GenericField):
    #TODO
    pass


# 5.65 Leg Time (LEG TIME)
def field_065(value):
    return '{}m {}s'.format(int(value[0]), int(value[1])*6)


# 5.66 Station Declination (STN DEC)
class Field_5_066(Field_5_039):
    # No real difference.  039 wouldnt accept a 'G' ordinal, but
    # we let that slip in our decoder.
    pass


# 5.67 Threshold Crossing Height (TCH)
class Field_5_067(GenericField):
    #TODO
    pass


# 5.68 Landing Threshold Elevation (LANDING THRES ELEV)
class Field_5_068(GenericField):
    #TODO
    pass


# 5.69 Threshold Displacement Distance (DSPLCD THR)
class Field_5_069(GenericField):
    #TODO
    pass


# 5.70 Vertical Angle (VERT ANGLE)
class Field_5_070(GenericField):
    #TODO
    pass


# 5.71 Name Field
class Field_5_071(GenericField):
    #TODO
    pass


# 5.72 Speed Limit (SPEED LIMIT)
def field_072(value):
    if value.isnumeric():
        return value + " knots (IAS)"
    elif value.strip() == '':
        return value
    else:
        raise ValueError('Invalid speed' + value)


# 5.73 Speed Limit Altitude
def field_073(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.74 Component Elevation (GS ELEV, EL ELEV, AZ ELEV, BAZ ELEV)
class Field_5_074(GenericField):
    #TODO
    pass


# 5.75 From/To - Airport/Fix
class Field_5_075(GenericField):
    #TODO
    pass


# 5.76 Company Route Ident
class Field_5_076(GenericField):
    #TODO
    pass


# 5.77 VIA Code
class Field_5_077(GenericField):
    #TODO
    pass


# 5.78 SID/STAR/App/AWY (S/S/A/AWY) SID/STAR/Awy (S/S/AWY)
class Field_5_078(GenericField):
    #TODO
    pass


# 5.79 Stopway
class Field_5_079(GenericField):
    #TODO
    pass


# 5.80 ILS/MLS/GLS Category (CAT)
class Field_5_080(GenericField):
    #TODO
    pass


# 5.81 ATC Indicator (ATC)
class Field_5_081(GenericField):
    #TODO
    pass


# 5.82 Waypoint Usage
def field_082(value):
    wp = ''
    if value[1] == 'B':
        wp = wp + 'HI and LO Altitude'
    elif value[1] == 'H':
        wp = wp + 'HI Altitude'
    elif value[1] == 'L':
        wp = wp + 'LO Altitude'
    elif value[1] == ' ':
        wp = wp + 'Terminal Use Only'
    elif value[0] == 'R':
        wp = wp + 'RNAV'
    else:
        raise ValueError(f"Invalid Waypoint Usage: '{value}'")
    return wp


# 5.83 To FIX
class Field_5_083(GenericField):
    #TODO
    pass


# 5.84 RUNWAY TRANS
class Field_5_084(GenericField):
    #TODO
    pass


# 5.85 ENRT TRANS
class Field_5_085(GenericField):
    #TODO
    pass


# 5.86 Cruise Altitude
def field_086(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.87 Terminal/Alternate Airport (TERM/ALT ARPT)
class Field_5_087(GenericField):
    #TODO
    pass


# 5.88 Alternate Distance (ALT DIST)
class Field_5_088(GenericField):
    #TODO
    pass


# 5.89 Cost Index
class Field_5_089(GenericField):
    #TODO
    pass


# 5.90 ILS/DME Bias
class Field_5_090(GenericField):
    #TODO
    pass


# 5.91 Continuation Record Application Type (APPL)
def field_091(value):
    match value:
        case 'A':
            return 'Standard ARINC Continuation containing notes or other formatted data'
        case 'B':
            return 'Combined Controlling Agency/Call Sign and formatted Time of Operation'
        case 'C':
            return 'Call Sign/Controlling Agency Continuation'
        case 'E':
            return 'Primary Record Extension'
        case 'L':
            return 'VHF Navaid Limitation Continuation'
        case 'N':
            return 'Sector Narrative Continuation'
        case 'T':
            return 'Time of Operations Continuation "formatted time data"'
        case 'U':
            return 'Time of Operations Continuation "Narrative time data"'
        case 'V':
            return 'Time of Operations Continuation, Start/End Date'
        case 'P':
            return 'Flight Planning Application Continuation'
        case 'Q':
            return 'Flight Planning Application Primary Data Continuation'
        case 'S':
            return 'Simulation Application Continuation'
        case 'W':
            return 'Airport or Heliport Procedure Data Continuation with SBAS use authorization information'
        case _:
            return 'Unknown Application Type: ' + str(value)


# 5.92 Elevation (FAC ELEV)
def field_092(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.93 Facility Characteristics (FAC CHAR)
class Field_5_093(GenericField):
    #TODO
    pass


# 5.94 True Bearing (TRUE BRG)
class Field_5_094(GenericField):
    #TODO
    pass


# 5.95 Government Source (SOURCE)
class Field_5_095(GenericField):
    #TODO
    pass


# 5.96 Glide Slope Beam Width (GS BEAM WIDTH)
class Field_5_096(GenericField):
    #TODO
    pass


# 5.97 Touchdown Zone Elevation (TDZE)
class Field_5_097(GenericField):
    #TODO
    pass


# 5.98 ‘TDZE Location (LOCATION)
class Field_5_098(GenericField):
    #TODO
    pass


# 5.99 Marker Type (MKR TYPE)
class Field_5_099(GenericField):
    #TODO
    pass


# 5.100 Minor Axis Bearing (MINOR AXIS TRUE BRG)
class Field_5_100(GenericField):
    #TODO
    pass


# 5.101 Communications Type (COMM TYPE)
def field_101(value):
    d = defaultdict(def_val)
    d['ACC'] = 'Area Control Center'
    d['ACP'] = 'Airlift Command Post'
    d['AIR'] = 'Air to Air'
    d['APP'] = 'Approach Control'
    d['ARR'] = 'Arrival Control'
    d['ASO'] = 'Automatic Surface Observing System (ASOS)'
    d['ATI'] = 'Automatic Terminal Info Service (ATIS)'
    d['AWI'] = 'Airport Weather Information Broadcast (AWIB)'
    d['AWO'] = 'Automatic Weather Observing Service (AWOS)'
    d['AWS'] = 'Aerodrome Weather Information Services (AWIS)'
    d['CLD'] = 'Clearance Delivery'
    d['CPT'] = 'Clearance, Pre-Taxi'
    d['CTA'] = 'Control Area (Terminal)'
    d['CTL'] = 'Control'
    d['DEP'] = 'Departure Control'
    d['DIR'] = 'Director (Approach Control Radar)'
    d['EFS'] = 'Enroute Flight Advisory Service (EFAS)'
    d['EMR'] = 'Emergency'
    d['FSS'] = 'Flight Service Station'
    d['GCO'] = 'Ground Comm Outlet'
    d['GND'] = 'Ground Control'
    d['GTE'] = 'Gate Control'
    d['HEL'] = 'Helicopter Frequency'
    d['INF'] = 'Information'
    d['MIL'] = 'Military Frequency'
    d['MUL'] = 'Multicom'
    d['OPS'] = 'Operations'
    d['PAL'] = 'Pilot Activated Lighting (Note 1)'
    d['RDO'] = 'Radio'
    d['RDR'] = 'Radar'
    d['RFS'] = 'Remote Flight Service Station (RFSS)'
    d['RMP'] = 'Ramp/Taxi Control'
    d['RSA'] = 'Airport Radar Service Area (ARSA)'
    d['TCA'] = 'Terminal Control Area'
    d['TMA'] = 'Terminal Control Area'
    d['TML'] = 'Terminal'
    d['TRS'] = 'Terminal Radar Service Area (TRSA)'
    d['TWE'] = 'Transcribe Weather Broadcast (TWEB)'
    d['TWR'] = 'Tower, Air Traffic Control'
    d['UAC'] = 'Upper Area Control'
    d['UNI'] = 'Unicom'
    d['VOL'] = 'Volmet'
    return d[value] if d[value] != "bad value" else value + "BAD VALUE"


# 5.102 Radar (RADAR)
def field_102(value):
    match value:
        case 'R':
            return 'Radar Capabilities'
        case 'N':
            return 'No Radar Capabilities'
        case _:
            return value


# 5.103 ‘Communications Frequency (COMM FREQ)
def field_103(value):
    if (value.isnumeric()):
        return "{:.2f}".format(float(value)/100)
    else:
        return "BAD VALUE"


# 5.104 Frequency Units (FREQ UNIT)
def field_104(value):
    d = defaultdict(def_val)
    d['H'] = 'High Frequency (3000 kHz - 30,000 kHz)'
    d['V'] = 'Very High Frequency (30,000 kHz - 200 MHz)'
    d['U'] = 'Ultra High Frequency (200 MHz - 3000 MHz)'
    d['C'] = 'Communication Channel for 8.33 kHz spacing'
    return d[value] if d[value] != "bad value" else value + "BAD VALUE"


# 5.105 Call Sign (CALL SIGN)
class Field_5_105(GenericField):
    #TODO
    pass


# 5.106 Service Indicator (SER IND)
def field_106(value):
    if (value.strip() == ''):
        return value
    sections = defaultdict(def_val)
    sections['A  '] = 'Airport Advisory Serivce (AAS)'
    sections['C  '] = 'Community Aerodrome Radio Station (CARS)'
    sections['D  '] = 'Departure Service (Other than Departure Control Unit)'
    sections['F  '] = 'Flight Information Serivce (FIS)'
    sections['I  '] = 'Initial Contact (IC)'
    sections['L  '] = 'Arrival Service (Other than Arrival Control Unit)'
    sections['P  '] = 'Pre-Departure Clearance (Data Link Service)'
    sections['S  '] = 'Aerodrome Flight Information Service (AFIS)'
    sections['T  '] = 'Terminal Area Control (Other than dedicated Terminal Control Unit)'
    sections[' A '] = 'Aerodrome Traffic Frequency (ATF)'
    sections[' C '] = 'Common Traffic Advisory Frequency (CTAF)'
    sections[' M '] = 'Mandatory Frequency (MF) '
    sections[' R '] = 'Air/Air'
    sections[' S '] = 'Secondary Frequency'
    sections['  A'] = 'Air/Ground'
    sections['  D'] = 'VHF Direction Finding Service (VDF)'
    sections['  G'] = 'Remote Communications Air to Ground (RCAG)'
    sections['  L'] = 'Language other than English'
    sections['  M'] = 'Military Use Frequency'
    sections['  P'] = 'Pilot Controlled Light (PCL)'
    sections['  R'] = 'Remote Communications Outlet (RCO)'
    return sections[value]


# 5.107 ATAMIATA Designator (ATA/IATA)
class Field_5_107(GenericField):
    #TODO
    pass


# 5.108 IFR Capability (IFR)
def field_108(value):
    match value:
        case 'Y':
            return 'Official'
        case 'N':
            return 'Non-official'
        case _:
            raise ValueError('Invalid IFR Capability')


# 5.109 Runway Width (WIDTH)
class Field_5_109(GenericField):
    #TODO
    pass


# 5.110 Marker Ident (MARKER IDENT)
class Field_5_110(GenericField):
    #TODO
    pass


# 5.111 Marker Code (MARKER CODE)
class Field_5_111(GenericField):
    #TODO
    pass


# 5.112 Marker Shape (SHAPE)
def field_112(value):
    match value:
        case 'E':
            return 'Elliptical'
        case 'B':
            return 'Bone'
        case _:
            return value


# 5.113 High/Low (HIGH/LOW)
def field_113(value):
    match value:
        case 'H':
            return 'High Power (general use)'
        case 'L':
            return 'Low Power (low altitude use)'
        case _:
            return value


# 5.114 Duplicate Identifier (DUP IND)
class Field_5_114(GenericField):
    #TODO
    pass


# 5.115 Direction Restriction
class Field_5_115(GenericField):
    #TODO
    pass


# 5.116 FIR/UIR Identifier (FIR/UIR IDENT)
class Field_5_116(GenericField):
    #TODO
    pass


# 5.117 FIR/UIR Indicator (IND)
def field_117(value):
    if value == 'F':
        return 'FIR'
    elif value == 'U ':
        return 'UIR'
    elif value == 'B':
        return 'Combined FIR/UIR'
    else:
        print("FIR UNKNOWN:", value)
        # raise ValueError("Invalid FIR/UIR Indicator")


# 5.118 Boundary Via (BDRY VIA)
class Field_5_118(StrTableWDefault):
    UNKNOWN =    (auto(), '<UNKNOWN>')
    CIRC =       ('C ', 'Circle')
    GCIRC =      ('G ', 'Great Circle')
    RHUMB =      ('H ', 'Rhumb Line')
    CCWARC =     ('L ', 'Counter Clockwise ARC')
    CWARC =      ('R ', 'Clockwise ARC')
    CIRC_RET =   ('CE', 'Circle, Returning to origin')
    GCIRC_RET =  ('GE', 'Great Circle, Returning to origin')
    RHUMB_RET =  ('HE', 'Rhumb Line, Returning to origin')
    CCWARC_RET = ('LE', 'Counter Clockwise ARC, Returning to origin')
    CWARC_RET =  ('RE', 'Clockwise ARC, Returning to origin')

# 5.119 Arc Distance (ARC DIST)
class Field_5_119(FixedReal):
    # CWWWF is the format with WWWF being digits, and F being the
    # floating point portion of the number. C is the DeclnCardinal portion.
    dplaces = 1
    valpos = range(0,4)


# 5.120 ‘Arc Bearing (ARC BRG)
class Field_5_120(FixedRealDegrees):
    dplaces = 1
    valpos = range(0,4)


# 5.121 Lower/Upper Limit
class Field_5_121(GenericField):
    #TODO
    pass


# 5.122 FIR/UIR ATC Reporting Units Speed (RUS)
class Field_5_122(GenericField):
    #TODO
    pass


# 5.123 FIR/UIR ATC Reporting Units Altitude (RUA)
def field_123(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.124 FIR/UIR Entry Report (ENTRY)
class Field_5_124(GenericField):
    #TODO
    pass


# 5.125 FIR/UIR Name
class Field_5_125(GenericField):
    #TODO
    pass


# 5.126 Restrictive Airspace Name
class Field_5_126(GenericField):
    #TODO
    pass


# 5.127 Maximum Altitude (MAX ALT)
def field_127(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.128 Restrictive Airspace Type (REST TYPE)
class Field_5_128(GenericField):
    #TODO
    pass


# 5.129 Restrictive Airspace Designation
class Field_5_129(GenericField):
    #TODO
    pass


# 5.130 Multiple Code (MULTI CD)
class Field_5_130(GenericField):
    #TODO
    pass


# 5.131 Time Code (TIME CD)
class Field_5_131(GenericField):
    #TODO
    pass


# 5.132 NOTAM
class Field_5_132(GenericField):
    #TODO
    pass


# 5.133 Unit Indicator (UNIT IND)
class Field_5_133(GenericField):
    #TODO
    pass


# 5.134 Cruise Table Identifier (CRSE TBL IDENT)
class Field_5_134(GenericField):
    #TODO
    pass


# 5.135 Course FROM/TO.
def field_135(value):
    if (value.isnumeric()):
        return float(value)/10
    else:
        return "BAD VALUE"


# 5.136 Cruise Level From/To
class Field_5_136(GenericField):
    #TODO
    pass


# 5.137 Vertical Separation
class Field_5_137(GenericField):
    #TODO
    pass


# 5.138 Time Indicator (TIME IND)
class Field_5_138(GenericField):
    #TODO
    pass


# 5.139 Intentionally Left Blank
class Field_5_139(GenericField):
    #TODO
    pass


# 5.140 Controlling Agency
class Field_5_140(GenericField):
    #TODO
    pass


# 5.141 Starting Latitude
class Field_5_141_5_142(Field_5_036_5_037):
    def __init__(self, text = None, latLon = None):
        if ((text is None) and (latLon is None)):
            raise ValueError("text or geodest arg req'd")
        if (text is None):
            self.geodesy = latLon
            return
        self.lat_card = CardinalDir(text[0])
        self.lon_card = CardinalDir(text[3])
        self.latitude = int(text[1:3]) * self.lat_card.lat_mul
        self.longitude = int(text[4:7]) * self.lon_card.lon_mul

    @classmethod
    def validate(cls, latlon):
        if ((latlon[0] not in ['N', 'S', 'n', 's'])
            or (latlon[3] not in ['E', 'W', 'e', 'w'])
            or (latlon[1:3].isnumeric() is not True)
            or (latlon[4:7].isnumeric() is not True)
            or (int(latlon[1:3]) > 90)
            or (int(latlon[4:7]) > 180)):
            return False
        return True

# 5.143 Grid MORA,
class Field_5_143(GenericField):
    #TODO
    pass


# 5.144 Center Fix (CENTER FIX)
class Field_5_144(GenericField):
    #TODO
    pass


# 5.145 Radius Li
class Field_5_145(GenericField):
    #TODO
    pass


# 5.146 Sector Bearing (SEC BRG)
class Field_5_146(GenericField):
    #TODO
    pass


# 5.147 Sector Altitude (SEC ALT)
def field_147(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.148 Enroute Alternate Airport (EAA)
class Field_5_148(GenericField):
    #TODO
    pass


# 5.149 Figure of Merit (MERIT)
class Field_5_149(GenericField):
    #TODO
    pass


# 5.150 Frequency Protection Distance (FREQ PRD)
class Field_5_150(GenericField):
    #TODO
    pass


# 5.151 FIR/UIR Address (ADDRESS)
class Field_5_151(GenericField):
    #TODO
    pass


# 5.152 Start/End Indicator (S/E IND)
class Field_5_152(GenericField):
    #TODO
    pass


# 5.153 Start/End Date
class Field_5_153(GenericField):
    #TODO
    pass


# 5.154 Restriction Identifier (REST IDENT)
class Field_5_154(GenericField):
    #TODO
    pass


# 5.155 Intentionally Left Blank
class Field_5_155(GenericField):
    #TODO
    pass


# 5.156 Intentionally Left Blank
class Field_5_156(GenericField):
    #TODO
    pass


# 5.157 Airway Restriction Start/End Date (START/END DATE)
class Field_5_157(GenericField):
    #TODO
    pass


# 5.158 Intentionally Left Blank
class Field_5_158(GenericField):
    #TODO
    pass


# 5.159 Intentionally Left Blank
class Field_5_159(GenericField):
    #TODO
    pass


# 5.160 Units of Altitude (UNIT IND)
class Field_5_160(GenericField):
    #TODO
    pass


# 5.161 Restriction Altitude (REST ALT)
def field_161(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.162 Step Climb Indicator (STEP)
class Field_5_162(GenericField):
    #TODO
    pass


# 5.163 Restriction Notes
class Field_5_163(GenericField):
    #TODO
    pass


# 5.164 EU Indicator (EU IND)
class Field_5_164(GenericField):
    #TODO
    pass


# 5.165 Magnetic/True Indicator (M/T IND)
def field_165(value):
    if value == 'M':
        return 'Magnetic'
    elif value == 'T':
        return 'True'
    else:
        return value


# 5.166 Channel
class Field_5_166(GenericField):
    #TODO
    pass


# 5.167 MLS Azimuth Bearing (MLS AZ BRG) MLS Back Azimuth Bearing (MLS BAZ BRG)
class Field_5_167(GenericField):
    #TODO
    pass


# 5.168 Azimuth Proportional Angle Right/Left (AZ PRO RIGHT/LEFT)
# Back Azimuth Proportional Angle Right/Left (BAZ PRO RIGHT/LEFT)
class Field_5_168(GenericField):
    #TODO
    pass


# 5.169 Elevation Angle Span (EL ANGLE SPAN)
class Field_5_169(GenericField):
    #TODO
    pass


# 5.170 Decision Height (DH)
class Field_5_170(GenericField):
    #TODO
    pass


# 5.171 Minimum Descent Height (MDH)
class Field_5_171(GenericField):
    #TODO
    pass


# 5.172 Azimuth Coverage Sector Right/Left (AZ COV RIGHT/LEFT) Back Azimuth Coverage Sector Right/Left (BAZ COV RIGHT/LEFT)
class Field_5_172(GenericField):
    #TODO
    pass


# 5.173 Nominal Elevation Angle (NOM ELEV ANGLE)
class Field_5_173(GenericField):
    #TODO
    pass


# 5.174 Restrictive Airspace Link Continuation (LC)
class Field_5_174(GenericField):
    #TODO
    pass


# 5.175 Holding Speed (HOLD SPEED)
class Field_5_175(GenericField):
    #TODO
    pass


# 5.176 Pad Dimensions
class Field_5_176(GenericField):
    #TODO
    pass


# 5.177 Public/Military Indicator (PUB/MIL)
def field_177(value):
    match value:
        case 'C':
            return 'Public / Civil'
        case 'M':
            return 'Military'
        case 'P':
            return 'Private (not open to public)'
        case _:
            raise ValueError('Invalid Pub/Mil')


# 5.178 Time Zone
def field_178(value):
    if value[0].isalpha() and value[1:].isnumeric():
        x = string.ascii_uppercase.index(value[0]) - 12
        y = 'GMT +' + str(x) if x >= 0 else 'GMT -' + str(x)
        return y + ':' + str(value[1:])
    else:
        print("TZ UNKNOWN:", value)


# 5.179 Daylight Time Indicator (DAY TIME)
def field_179(value):
    match value:
        case 'Y':
            return 'Yes'
        case 'N':
            return 'No'
        case _:
            print("DTI UNKNOWN:", value)


# 5.180 Pad Identifier (PAD IDENT)
class Field_5_180(GenericField):
    #TODO
    pass


# 5.181 H24 Indicator (H24)
def field_181(value):
    d = defaultdict(def_val)
    d['Y'] = '24-Hour Availability'
    d['N'] = 'Part-time Availability'
    return d[value] if d[value] != "bad value" else value + "BAD VALUE"


# 5.182 Guard/Transmit (G/T)
def field_182(value):
    match value:
        case 'G':
            return "Guard (radio receives on this freq)"
        case 'T':
            return "Transmit (radio transmits on this freq)"
        case ' ':
            return "Guards and Transmits"
        case _:
            raise ValueError("bad guard/transmit")


# 5.183 Sectorization (SECTOR)
class Field_5_183(GenericField):
    #TODO
    pass


# 5.184 Communication Altitude (COMM ALTITUDE)
def field_184(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.185 Sector Facility (SEC FAC)
class Field_5_185(GenericField):
    #TODO
    pass


# 5.186 Narrative
class Field_5_186(GenericField):
    #TODO
    pass


# 5.187 Distance Description (DIST DESC)
class Field_5_187(GenericField):
    #TODO
    pass


# 5.188 Communications Distance (COMM DIST)
class Field_5_188(GenericField):
    #TODO
    pass


# 5.189 Remote Site Name
class Field_5_189(GenericField):
    #TODO
    pass


# 5.190 FIR/RDO Identifier (FIR/RDO)
class Field_5_190(GenericField):
    #TODO
    pass


# 5.191 Triad Stations (TRIAD STA)
class Field_5_191(GenericField):
    #TODO
    pass


# 5.192 Group Repetition Interval (GRI)
class Field_5_192(GenericField):
    #TODO
    pass


# 5.193 Additional Secondary Phase Factor (ASF)
class Field_5_193(GenericField):
    #TODO
    pass


# 5.194 Initial/Terminus Airport/Fix
class Field_5_194(GenericField):
    #TODO
    pass


# 5.195 Time of Operation
class Field_5_195(GenericField):
    #TODO
    pass


# 5.196 Name Format Indicator (NAME IND)
def field_196(value):
    match value[0]:
        case 'A':
            return 'Abeam Fix'
        case 'B':
            return 'Bearing and Distance Fix '
        case 'D':
            return 'Airport Name as Fix'
        case 'F':
            return 'FIR Fix'
        case 'H':
            return 'Phonetic Letter Name Fix'
        case 'I':
            return 'Airport Ident as Fix'
        case 'L':
            return 'Latitude/Longitude Fix '
        case 'M':
            return 'Multiple Word Name Fix'
        case 'N':
            return 'Navaid Ident as Fix'
        case 'P':
            return 'Published Five - Letter - Name - Fix'
        case 'Q':
            return 'Published Name Fix, less than five letters'
        case 'R':
            return 'Published Name Fix, more than five letters'
        case 'T':
            return 'Airport/Rwy Related Fix (Note 2)'
        case 'U':
            return 'UIR Fix'
    match value[1]:
        case 'O':
            return 'Localizer Marker with officially published five - letter identifier'
        case 'M':
            return 'Localizer Marker without officially published five - letter identifier'
        case _:
            return 'Unknown Name Format Indicator'


# 5.197 Datum Code (DATUM)
class Field_5_197(GenericField):
    #TODO
    pass


# 5.198 Modulation (MODULN)
def field_198(value):
    d = defaultdict(def_val)
    d['A'] = 'Amplitude Modulated'
    d['F'] = 'Frequency Modulated'
    return d[value] if d[value] != "bad value" else value + "BAD VALUE"


# 5.199 Signal Emission (SIG EM)
def field_199(value):
    if value.strip() == '':
        return value
    d = defaultdict(def_val)
    d['3'] = 'Double Sideband (A3) '
    d['A'] = 'Single sideband, reduced carrier (A3A) '
    d['B'] = 'Two Independent sidebands (A3B)'
    d['H'] = 'Single sideband, full carrier (A3H) '
    d['J'] = 'Single sideband, suppressed carrier (A3J)'
    d['L'] = 'Lower (single) sideband, carrier unknown'
    d['U'] = 'Upper (single) sideband, carrier unknown'
    return d[value] if d[value] != "bad value" else value + "BAD VALUE"


# 5.200 Remote Facility (REM FAC)
class Field_5_200(GenericField):
    #TODO
    pass


# 5.201 Restriction Record Type (REST TYPE)
class Field_5_201(GenericField):
    #TODO
    pass


# 5.202 Exclusion Indicator (EXC IND)
class Field_5_202(GenericField):
    #TODO
    pass


# 5.203 Block Indicator (BLOCK IND)
class Field_5_203(GenericField):
    #TODO
    pass


# 5.204 ARC Radius (ARC RAD)
class Field_5_204(GenericField):
    #TODO
    pass


# 5.205 Navaid Limitation Code (NLC)
class Field_5_205(GenericField):
    #TODO
    pass


# 5.206 Component Affected Indicator (COMP AFFTD IND)
class Field_5_206(GenericField):
    #TODO
    pass


# 5.207 Sector From/Sector To (SECTR)
class Field_5_207(GenericField):
    #TODO
    pass


# 5.208 Distance Limitation (DIST LIMIT)
class Field_5_208(GenericField):
    #TODO
    pass


# 5.209 Altitude Limitation (ALT LIMIT)
def field_209(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.210 Sequence End Indicator (SEQ END)
class Field_5_210(GenericField):
    #TODO
    pass


# 5.211 Required Navigation Performance (RNP)
class Field_5_211(GenericField):
    #TODO
    pass


# 5.212 Runway Gradient (RWY GRAD)
class Field_5_212(GenericField):
    #TODO
    pass


# 5.213 Controlled Airspace Type (ARSP TYPE)
class Field_5_213(GenericField):
    #TODO
    pass


# 5.214 Controlled Airspace Center (ARSP CNTR)
class Field_5_214(GenericField):
    #TODO
    pass


# 5.215 Controlled Airspace Classification (ARSP CLASS)
class Field_5_215(GenericField):
    #TODO
    pass


# 5.216 Controlled Airspace Name (ARSP NAME)
class Field_5_216(GenericField):
    #TODO
    pass


# 5.217 Controlled Airspace Indicator (CTLD ARSP IND)
class Field_5_217(GenericField):
    #TODO
    pass


# 5.218 Geographical Reference Table Identifier (GEO REF TBL ID)
class Field_5_218(GenericField):
    #TODO
    pass


# 5.219 Geographical Entity (GEO ENT)
class Field_5_219(GenericField):
    #TODO
    pass


# 5.220 Preferred Route Use Indicator (ET IND)
class Field_5_220(GenericField):
    #TODO
    pass


# 5.221 Aircraft Use Group (ACFT USE GP)
class Field_5_221(GenericField):
    #TODO
    pass


# 5.222 GNSS/FMS Indicator (GNSS/FMS IND)
class Field_5_222(GenericField):
    #TODO
    pass


# 5.223 Operations Type (OPS TYPE)
class Field_5_223(GenericField):
    #TODO
    pass


# 5.224 Route Indicator (RTE IND)
class Field_5_224(GenericField):
    #TODO
    pass


# 5.225 Ellipsoidal Height
class Field_5_225(GenericField):
    #TODO
    pass


# 5.226 Glide Path Angle (GPA)
class Field_5_226(GenericField):
    #TODO
    pass


# 5.227 Orthometric Height (ORTH HGT)
class Field_5_227(GenericField):
    #TODO
    pass


# 5.228 Course Width at Threshold (CRSWDTH)
class Field_5_228(GenericField):
    #TODO
    pass


# 5.229 Final Approach Segment DATA CRC Remainder (FAS CRC)
class Field_5_229(GenericField):
    #TODO
    pass


# 5.230 Procedure Type (PROC TYPE)
class Field_5_230(GenericField):
    #TODO
    pass


# 5.231 Along Track Distance (ATD)
class Field_5_231(GenericField):
    #TODO
    pass


# 5.232 Number of Engines Restriction (NOE)
class Field_5_232(GenericField):
    #TODO
    pass


# 5.233 Turboprop/Jet Indicator (TURBO)
class Field_5_233(GenericField):
    #TODO
    pass


# 5.234 RNAV Flag (RNAV)
class Field_5_234(GenericField):
    #TODO
    pass


# 5.235 ATC Weight Category (ATC WC)
class Field_5_235(GenericField):
    #TODO
    pass


# 5.236 ATC Identifier (ATC ID)
class Field_5_236(GenericField):
    #TODO
    pass


# 5.237 Procedure Description (PROC DESC)
class Field_5_237(GenericField):
    #TODO
    pass


# 5.238 Leg Type Code (LTC)
class Field_5_238(GenericField):
    #TODO
    pass


# 5.239 Reporting Code (RPT)
class Field_5_239(GenericField):
    #TODO
    pass


# 5.240 Altitude (ALT)
def field_240(value):
    return value.lstrip('0') + " ft" if value.isnumeric() else value


# 5.241 Fix Related Transition Code (FRT Code)
class Field_5_241(GenericField):
    #TODO
    pass


# 5.242 Procedure Category (PRO CAT)
class Field_5_242(GenericField):
    #TODO
    pass


# 5.243 GLS Station Identifier
class Field_5_243(GenericField):
    #TODO
    pass


# 5.244 GLS Channel
class Field_5_244(GenericField):
    #TODO
    pass


# 5.245 Service Volume Radius
class Field_5_245(GenericField):
    #TODO
    pass


# 5.246 TDMA Slots
class Field_5_246(GenericField):
    #TODO
    pass


# 5.247 Station Type
class Field_5_247(GenericField):
    #TODO
    pass


# 5.248 Station Elevation WGS84
class Field_5_248(GenericField):
    #TODO
    pass


# 5.249 Longest Runway Surface Code (LRSC)
class Field_5_249(GenericField):
    #TODO
    pass


# 5.250 Alternate Record Type (ART)
class Field_5_250(GenericField):
    #TODO
    pass


# 5.251 Distance To Alternate (DTA)
class Field_5_251(GenericField):
    #TODO
    pass


# 5.252 Alternate Type (ALT TYPE)
class Field_5_252(GenericField):
    #TODO
    pass


# 5.253 Primary and Additional Alternate Identifier (ALT IDENT)
class Field_5_253(GenericField):
    #TODO
    pass


# 5.254 Fixed Radius Transition Indicator (FIXED RAD IND)
class Field_5_254(GenericField):
    #TODO
    pass


# 5.255 SBAS Service Provider Identifier (SBAS ID)
class Field_5_255(GenericField):
    #TODO
    pass


# 5.256 Reference Path Data Selector (REF PDS)
class Field_5_256(GenericField):
    #TODO
    pass


# 5.257 Reference Path Identifier (REF ID)
class Field_5_257(GenericField):
    #TODO
    pass


# 5.258 Approach Performance Designator (APD)
class Field_5_258(GenericField):
    #TODO
    pass


# 5.259 Length Offset (OFFSET)
class Field_5_259(GenericField):
    #TODO
    pass


# 5.260 Terminal Procedure Flight Planning Leg Distance (LEG DIST)
class Field_5_260(GenericField):
    #TODO
    pass


# 5.261 Speed Limit Description (SLD)
class Field_5_261(GenericField):
    #TODO
    pass


# 5.262 Approach Type Identifier (ATI)
class Field_5_262(GenericField):
    #TODO
    pass


# 5.263 HAL
class Field_5_263(GenericField):
    #TODO
    pass


# 5.264 VAL
class Field_5_264(GenericField):
    #TODO
    pass


# 5.265 Path Point TCH
class Field_5_265(GenericField):
    #TODO
    pass


# 5.266 TCH Units Indicator
class Field_5_266(GenericField):
    #TODO
    pass


# 5.267 & 8 High Precision Latitude & Lon (HPLAT)
class Field_5_267_5_268(Field_5_036_5_037):
    def __init__(self, text = None, latLon = None):
        if ((text is None) and (latLon is None)):
            raise ValueError("text or geodest arg req'd")
        if (text is None):
            self.geodesy = latLon
            return
        self.lat_card = CardinalDir(text[0])
        self.lon_card = CardinalDir(text[11])
        self.latitude = (int(text[1:3]) + (int(text[3:5]) / 60) \
                         + (float(f"{text[5:7]}.{text[7:11]}") / 60**2)) \
                         * self.lat_card.lat_mul
        self.longitude = (int(text[12:15]) + (int(text[15:17]) / 60) \
                          + (float(f"{text[17:19]}.{text[19:23]}") / 60**2)) \
                          * self.lon_card.lon_mul

    @classmethod
    def validate(cls, latlon):
        if ((latlon[0] not in ['N', 'S', 'n', 's'])
            or (latlon[11] not in ['E', 'W', 'e', 'w'])
            or (latlon[1:11].isnumeric() is not True)
            or (latlon[12:23].isnumeric() is not True)
            or (int(latlon[1:11]) > 9000000000)
            or (int(latlon[3:11]) > 60000000)
            or (int(latlon[5:11]) > 600000)
            or (int(latlon[12:23]) > 18000000000)
            or (int(latlon[15:23]) > 60000000)
            or (int(latlon[17:23]) > 600000)):
            return False
        return True


# 5.269 Helicopter Procedure Course (HPC)
def field_269(value):
    if (value.isnumeric()):
        return int(value)
    elif (value == "   "):
        return float('nan') # '   ' is /Not a Number, but valid for a -23 rec.
    else:
        raise ValueError(f'Bad Helicopter Procedure Course: {value}')


# 5.270 TCH Value Indicator (TCHVI)
def field_270(value):
    match value:
        case 'I':
            return 'ILS or MLS Glideslope'
        case 'R':
            return 'RNAV Procedure'
        case 'V':
            return 'Visual Glideslope Indicator (VGSI)'
        case 'D':
            return 'Default Value (40 or 50 feet)'
        case ' ':   # this is apparently allowed to be empty, see ARINC SPECIFICATION 424 - Page 165
            return value
        case _:
            raise ValueError(f'Bad TCH Value Indicator: {value}')


# 5.271 Procedure Turn (PROC TURN)
class Field_5_271(GenericField):
    #TODO
    pass


# 5.272 TAA Sector Identifier
class Field_5_272(GenericField):
    #TODO
    pass


# 5.273 TAA IAF Waypoint
class Field_5_273(GenericField):
    #TODO
    pass


# 5.274 TAA Sector Radius
class Field_5_274(GenericField):
    #TODO
    pass


# 5.275 Level of Service Name (LSN)
class Field_5_275(GenericField):
    #TODO
    pass


# 5.276 ??
class Field_5_276(GenericField):
    #TODO
    pass


# 5.320 SBAS Final Approach Course
class Field_5_320(GenericField):
    #TODO
    pass


