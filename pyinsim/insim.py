# insim.py - InSim.txt replacement for pyinsim
#
# Copyright 2008-2015 Alex McBride <xandermcbride@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 3 or any later version.
#

import struct
import math

__all__ = ['BFN_CLEAR', 'BFN_DEL_BTN', 'BFN_REQUEST', 'BFN_USER_CLEAR', 'CAR_ALL', 'CAR_BF1', 'CAR_FBM', 'CAR_FO8', 'CAR_FOX', 'CAR_FXO', 'CAR_FXR', 'CAR_FZ5', 'CAR_FZR', 'CAR_LX4', 'CAR_LX6', 'CAR_MRT', 'CAR_NONE', 'CAR_RAC', 'CAR_RB4', 'CAR_UF1', 'CAR_UFR', 'CAR_XFG', 'CAR_XFR', 'CAR_XRG', 'CAR_XRR', 'CAR_XRT', 'CCI_BLUE', 'CCI_FIRST', 'CCI_LAG', 'CCI_LAST', 'CCI_YELLOW', 'CONF_CONFIRMED', 'CONF_DID_NOT_PIT', 'CONF_DISQ', 'CONF_MENTIONED', 'CONF_PENALTY_30', 'CONF_PENALTY_45', 'CONF_PENALTY_DT', 'CONF_PENALTY_SG', 'CONF_TIME', 'CarContOBJ', 'CarContact', 'CompCar', 'DL_ABS', 'DL_BATTERY', 'DL_FULLBEAM', 'DL_HANDBRAKE', 'DL_NUM', 'DL_OILWARN', 'DL_PITSPEED', 'DL_SHIFT', 'DL_SIGNAL_ANY', 'DL_SIGNAL_L', 'DL_SIGNAL_R', 'DL_SPARE', 'DL_TC', 'HInfo', 'HOSTF_CAN_RESET', 'HOSTF_CAN_SELECT', 'HOSTF_CAN_VOTE', 'HOSTF_CRUISE', 'HOSTF_FCV', 'HOSTF_MID_RACE', 'HOSTF_MUST_PIT', 'HOS_FIRST', 'HOS_LAST', 'HOS_LICENSED', 'HOS_S1', 'HOS_S2', 'HOS_SPECPASS', 'INSIM_VERSION', 'INST_ALWAYS_ON', 'IRP_ARP', 'IRP_ARQ', 'IRP_ERR', 'IRP_HLR', 'IRP_HOS', 'IRP_SEL', 'IR_ARP', 'IR_ARQ', 'IR_ERR', 'IR_ERR_ADMIN', 'IR_ERR_HOSTNAME', 'IR_ERR_NOSPEC', 'IR_ERR_PACKET', 'IR_ERR_PACKET2', 'IR_ERR_SPEC', 'IR_HLR', 'IR_HOS', 'IR_SEL', 'ISB_C1', 'ISB_C2', 'ISB_C4', 'ISB_CLICK', 'ISB_CTRL', 'ISB_DARK', 'ISB_LEFT', 'ISB_LIGHT', 'ISB_LMB', 'ISB_RIGHT', 'ISB_RMB', 'ISB_SHIFT', 'ISF_AXM_EDIT', 'ISF_AXM_LOAD', 'ISF_CON', 'ISF_HLV', 'ISF_LOCAL', 'ISF_MCI', 'ISF_MSO_COLS', 'ISF_NLP', 'ISF_OBH', 'ISF_RES_0', 'ISF_RES_1', 'ISP_ACR', 'ISP_AXI', 'ISP_AXM', 'ISP_AXO', 'ISP_BFN', 'ISP_BTC', 'ISP_BTN', 'ISP_BTT', 'ISP_CCH', 'ISP_CNL', 'ISP_CON', 'ISP_CPP', 'ISP_CPR', 'ISP_CRS', 'ISP_FIN', 'ISP_FLG', 'ISP_HLV', 'ISP_III', 'ISP_ISI', 'ISP_ISM', 'ISP_LAP', 'ISP_MCI', 'ISP_MOD', 'ISP_MSL', 'ISP_MSO', 'ISP_MST', 'ISP_MSX', 'ISP_MTC', 'ISP_NCN', 'ISP_NLP', 'ISP_NONE', 'ISP_NPL', 'ISP_OBH', 'ISP_PEN', 'ISP_PFL', 'ISP_PIT', 'ISP_PLA', 'ISP_PLC', 'ISP_PLL', 'ISP_PLP', 'ISP_PSF', 'ISP_REO', 'ISP_RES', 'ISP_RIP', 'ISP_RST', 'ISP_SCC', 'ISP_SCH', 'ISP_SFP', 'ISP_SMALL', 'ISP_SPX', 'ISP_SSH', 'ISP_STA', 'ISP_TINY', 'ISP_TOC', 'ISP_VER', 'ISP_VTN', 'ISS_16', 'ISS_FRONT_END', 'ISS_GAME', 'ISS_MPSPEEDUP', 'ISS_MULTI', 'ISS_PAUSED', 'ISS_REPLAY', 'ISS_SHIFTU', 'ISS_SHIFTU_FOLLOW', 'ISS_SHIFTU_NO_OPT', 'ISS_SHOW_2D', 'ISS_SOUND_MUTE', 'ISS_VIEW_OVERRIDE', 'ISS_VISIBLE', 'ISS_WINDOWED', 'IS_ACR', 'IS_AXI', 'IS_AXM', 'IS_AXO', 'IS_BFN', 'IS_BTC', 'IS_BTN', 'IS_BTT', 'IS_CCH', 'IS_CNL', 'IS_CON', 'IS_CPP', 'IS_CPR', 'IS_CRS', 'IS_FIN', 'IS_FLG', 'IS_HLV', 'IS_III', 'IS_ISI', 'IS_ISM', 'IS_LAP', 'IS_MCI', 'IS_MOD', 'IS_MSL', 'IS_MSO', 'IS_MST', 'IS_MSX', 'IS_MTC', 'IS_NCN', 'IS_NLP', 'IS_NPL', 'IS_OBH', 'IS_PEN', 'IS_PFL', 'IS_PIT', 'IS_PLA', 'IS_PLC', 'IS_PLL', 'IS_PLP', 'IS_PSF', 'IS_REO', 'IS_RES', 'IS_RIP', 'IS_RST', 'IS_SCC', 'IS_SCH', 'IS_SFP', 'IS_SMALL', 'IS_SPX', 'IS_SSH', 'IS_STA', 'IS_TINY', 'IS_TOC', 'IS_VER', 'IS_VTN', 'LEAVR_BANNED', 'LEAVR_DISCO', 'LEAVR_KICKED', 'LEAVR_LOSTCONN', 'LEAVR_SECURITY', 'LEAVR_TIMEOUT', 'MSO_O', 'MSO_PREFIX', 'MSO_SYSTEM', 'MSO_USER', 'NodeLap', 'OBH_CAN_MOVE', 'OBH_LAYOUT', 'OBH_ON_SPOT', 'OBH_WAS_MOVING', 'OG_BAR', 'OG_CTRL', 'OG_KM', 'OG_SHIFT', 'OG_TURBO', 'ObjectInfo', 'OutGaugePack', 'OutSimPack', 'PENALTY_30', 'PENALTY_45', 'PENALTY_DT', 'PENALTY_DT_VALID', 'PENALTY_NONE', 'PENALTY_SG', 'PENALTY_SG_VALID', 'PENR_ADMIN', 'PENR_FALSE_START', 'PENR_SPEEDING', 'PENR_STOP_LATE', 'PENR_STOP_SHORT', 'PENR_UNKNOWN', 'PENR_WRONG_WAY', 'PIF_AUTOCLUTCH', 'PIF_AUTOGEARS', 'PIF_AXIS_CLUTCH', 'PIF_CUSTOM_VIEW', 'PIF_HELP_B', 'PIF_INPITS', 'PIF_KB_NO_HELP', 'PIF_KB_STABILISED', 'PIF_MOUSE', 'PIF_RESERVED_2', 'PIF_RESERVED_32', 'PIF_RESERVED_4', 'PIF_SHIFTER', 'PIF_SWAPSIDE', 'PITLANE_DT', 'PITLANE_ENTER', 'PITLANE_EXIT', 'PITLANE_NO_PURPOSE', 'PITLANE_SG', 'PMO_ADD_OBJECTS', 'PMO_CLEAR_ALL', 'PMO_DEL_OBJECTS', 'PMO_LOADING_FILE', 'PSE_BODY_MAJOR', 'PSE_BODY_MINOR', 'PSE_FR_DAM', 'PSE_FR_WHL', 'PSE_LE_FR_DAM', 'PSE_LE_FR_WHL', 'PSE_LE_RE_DAM', 'PSE_LE_RE_WHL', 'PSE_NOTHING', 'PSE_NUM', 'PSE_REFUEL', 'PSE_RE_DAM', 'PSE_RE_WHL', 'PSE_RI_FR_DAM', 'PSE_RI_FR_WHL', 'PSE_RI_RE_DAM', 'PSE_RI_RE_WHL', 'PSE_SETUP', 'PSE_STOP', 'RIPOPT_FULL_PHYS', 'RIPOPT_LOOP', 'RIPOPT_SKINS', 'RIP_ALREADY', 'RIP_CORRUPTED', 'RIP_DEDICATED', 'RIP_DEST_OOB', 'RIP_NOT_FOUND', 'RIP_NOT_REPLAY', 'RIP_OK', 'RIP_OOS', 'RIP_UNKNOWN', 'RIP_UNLOADABLE', 'RIP_USER', 'RIP_WRONG_MODE', 'SETF_ABS_ENABLE', 'SETF_SYMM_WHEELS', 'SETF_TC_ENABLE', 'SMALL_NLI', 'SMALL_NONE', 'SMALL_RTP', 'SMALL_SSG', 'SMALL_SSP', 'SMALL_STP', 'SMALL_TMS', 'SMALL_VTA', 'SND_ERROR', 'SND_INVALIDKEY', 'SND_MESSAGE', 'SND_SILENT', 'SND_SYSMESSAGE', 'SSH_CORRUPTED', 'SSH_DEDICATED', 'SSH_NO_SAVE', 'SSH_OK', 'TINY_AXC', 'TINY_AXI', 'TINY_CLOSE', 'TINY_CLR', 'TINY_GTH', 'TINY_ISM', 'TINY_MCI', 'TINY_MPE', 'TINY_NCN', 'TINY_NLP', 'TINY_NONE', 'TINY_NPL', 'TINY_PING', 'TINY_REN', 'TINY_REO', 'TINY_REPLY', 'TINY_RES', 'TINY_RIP', 'TINY_RST', 'TINY_SCP', 'TINY_SST', 'TINY_VER', 'TINY_VTC', 'TYRE_HYBRID', 'TYRE_KNOBBLY', 'TYRE_NOT_CHANGED', 'TYRE_R1', 'TYRE_R2', 'TYRE_R3', 'TYRE_R4', 'TYRE_ROAD_NORMAL', 'TYRE_ROAD_SUPER', 'VIEW_ANOTHER', 'VIEW_CAM', 'VIEW_CUSTOM', 'VIEW_DRIVER', 'VIEW_FOLLOW', 'VIEW_HELI', 'VOTE_END', 'VOTE_NONE', 'VOTE_QUALIFY', 'VOTE_RESTART']

INSIM_VERSION = 4
MAX_PLAYERS = 40


# Enum for packet types
ISP_NONE = 0
ISP_ISI = 1
ISP_VER = 2
ISP_TINY = 3
ISP_SMALL = 4
ISP_STA = 5
ISP_SCH = 6
ISP_SFP = 7
ISP_SCC = 8
ISP_CPP = 9
ISP_ISM = 10
ISP_MSO = 11
ISP_III = 12
ISP_MST = 13
ISP_MTC = 14
ISP_MOD = 15
ISP_VTN = 16
ISP_RST = 17
ISP_NCN = 18
ISP_CNL = 19
ISP_CPR = 20
ISP_NPL = 21
ISP_PLP = 22
ISP_PLL = 23
ISP_LAP = 24
ISP_SPX = 25
ISP_PIT = 26
ISP_PSF = 27
ISP_PLA = 28
ISP_CCH = 29
ISP_PEN = 30
ISP_TOC = 31
ISP_FLG = 32
ISP_PFL = 33
ISP_FIN = 34
ISP_RES = 35
ISP_REO = 36
ISP_NLP = 37
ISP_MCI = 38
ISP_MSX = 39
ISP_MSL = 40
ISP_CRS = 41
ISP_BFN = 42
ISP_AXI = 43
ISP_AXO = 44
ISP_BTN = 45
ISP_BTC = 46
ISP_BTT = 47
ISP_RIP = 48
ISP_SSH = 49
ISP_CON = 50
ISP_OBH = 51
ISP_HLV = 52
ISP_PLC = 53
ISP_AXM = 54
ISP_ACR = 55

# Relay packets.
IRP_ARQ = 250
IRP_ARP = 251
IRP_HLR = 252
IRP_HOS = 253
IRP_SEL = 254
IRP_ERR = 255

# Enum for IS_TINY sub-type
TINY_NONE = 0
TINY_VER = 1
TINY_CLOSE = 2
TINY_PING = 3
TINY_REPLY = 4
TINY_VTC = 5
TINY_SCP = 6
TINY_SST = 7
TINY_GTH = 8
TINY_MPE = 9
TINY_ISM = 10
TINY_REN = 11
TINY_CLR = 12
TINY_NCN = 13
TINY_NPL = 14
TINY_RES = 15
TINY_NLP = 16
TINY_MCI = 17
TINY_REO = 18
TINY_RST = 19
TINY_AXI = 20
TINY_AXC = 21
TINY_RIP = 22
TINY_NCI = 23

# Enum for IS_SMALL sub-type
SMALL_NONE = 0
SMALL_SSP = 1
SMALL_SSG = 2
SMALL_VTA = 3
SMALL_TMS = 4
SMALL_STP = 5
SMALL_RTP = 6
SMALL_NLI = 7

# Bit flags for ISI Flags
ISF_RES_0 = 1
ISF_RES_1 = 2
ISF_LOCAL = 4
ISF_MSO_COLS = 8
ISF_NLP = 16
ISF_MCI = 32
ISF_CON = 64
ISF_OBH = 128
ISF_HLV = 256
ISF_AXM_LOAD = 512
ISF_AXM_EDIT = 1024

# Enum for IS_MSO UserType
MSO_SYSTEM = 0
MSO_USER = 1
MSO_PREFIX = 2
MSO_O = 3

# Enum for IS_MSL Sound
SND_SILENT = 0
SND_MESSAGE = 1
SND_SYSMESSAGE = 2
SND_INVALIDKEY = 3
SND_ERROR = 4

# Enum for IS_VTN Action
VOTE_NONE = 0
VOTE_END = 1
VOTE_RESTART = 2
VOTE_QUALIFY = 3

# Enum for IS_PLA Fact
PITLANE_EXIT = 0
PITLANE_ENTER = 1
PITLANE_NO_PURPOSE = 2
PITLANE_DT = 3
PITLANE_SG = 4

# Enum for IS_STA InGameCam
VIEW_FOLLOW = 0
VIEW_HELI = 1
VIEW_CAM = 2
VIEW_DRIVER = 3
VIEW_CUSTOM = 4
VIEW_ANOTHER = 255

# Enum for IS_CNL Reason
LEAVR_DISCO = 0
LEAVR_TIMEOUT = 1
LEAVR_LOSTCONN = 2
LEAVR_KICKED = 3
LEAVR_BANNED = 4
LEAVR_SECURITY = 5
LEAVR_CPW = 6
LEAVR_OOS = 7
LEAVR_JOOS = 8
LEAVR_HACK = 9

# Enum for IS_PEN Penalty
PENALTY_NONE = 0
PENALTY_DT = 1
PENALTY_DT_VALID = 2
PENALTY_SG = 3
PENALTY_SG_VALID = 4
PENALTY_30 = 5
PENALTY_45 = 6

# Enum for IS_PEN Reason
PENR_UNKNOWN = 1
PENR_ADMIN = 2
PENR_WRONG_WAY = 3
PENR_FALSE_START = 4
PENR_SPEEDING = 5
PENR_STOP_SHORT = 6
PENR_STOP_LATE = 7

# Enum for IS_PIT Tyres
TYRE_R1 = 0
TYRE_R2 = 1
TYRE_R3 = 2
TYRE_R4 = 3
TYRE_ROAD_SUPER = 4
TYRE_ROAD_NORMAL = 5
TYRE_HYBRID = 6
TYRE_KNOBBLY = 7
TYRE_NOT_CHANGED = 255

# Bit flags for IS_STA Flags
ISS_GAME = 1
ISS_REPLAY = 2
ISS_PAUSED = 4
ISS_SHIFTU = 8
ISS_16 = 16
ISS_SHIFTU_FOLLOW = 32
ISS_SHIFTU_NO_OPT = 64
ISS_SHOW_2D = 128
ISS_FRONT_END = 256
ISS_MULTI = 512
ISS_MPSPEEDUP =    1024
ISS_WINDOWED = 2048
ISS_SOUND_MUTE = 4096
ISS_VIEW_OVERRIDE = 8192
ISS_VISIBLE = 16384

# Bit flags for IS_PIT Work
PSE_NOTHING = 1
PSE_STOP = 2
PSE_FR_DAM = 4
PSE_FR_WHL = 8
PSE_LE_FR_DAM = 16
PSE_LE_FR_WHL = 32
PSE_RI_FR_DAM = 64
PSE_RI_FR_WHL = 128
PSE_RE_DAM = 256
PSE_RE_WHL = 512
PSE_LE_RE_DAM = 1024
PSE_LE_RE_WHL = 2048
PSE_RI_RE_DAM = 4096
PSE_RI_RE_WHL = 8192
PSE_BODY_MINOR = 16384
PSE_BODY_MAJOR = 32768
PSE_SETUP = 65536
PSE_REFUEL = 131072
PSE_NUM = 262144

# Bit flags for IS_NPL Flags
PIF_SWAPSIDE = 1
PIF_RESERVED_2 = 2
PIF_RESERVED_4 = 4
PIF_AUTOGEARS = 8
PIF_SHIFTER = 16
PIF_RESERVED_32 = 32
PIF_HELP_B = 64
PIF_AXIS_CLUTCH = 128
PIF_INPITS = 256
PIF_AUTOCLUTCH = 512
PIF_MOUSE = 1024
PIF_KB_NO_HELP = 2048
PIF_KB_STABILISED = 4096
PIF_CUSTOM_VIEW = 8192

# Bit flags for IS_RES Confirm
CONF_MENTIONED = 1
CONF_CONFIRMED = 2
CONF_PENALTY_DT = 4
CONF_PENALTY_SG = 8
CONF_PENALTY_30 = 16
CONF_PENALTY_45 = 32
CONF_DID_NOT_PIT = 64
CONF_DISQ = CONF_PENALTY_DT | CONF_PENALTY_SG | CONF_DID_NOT_PIT
CONF_TIME = CONF_PENALTY_30 | CONF_PENALTY_45

# Bit flags for IS_RST Flags
HOSTF_CAN_VOTE = 1
HOSTF_CAN_SELECT = 2
HOSTF_MID_RACE = 32
HOSTF_MUST_PIT = 64
HOSTF_CAN_RESET = 128
HOSTF_FCV = 256
HOSTF_CRUISE = 512

# Bit flags for CompCar Info
CCI_BLUE = 1
CCI_YELLOW = 2
CCI_LAG    = 32
CCI_FIRST = 64
CCI_LAST = 128

# Enum for IS_BFN SubT
BFN_DEL_BTN = 0
BFN_CLEAR = 1
BFN_USER_CLEAR = 2
BFN_REQUEST = 3
INST_ALWAYS_ON = 128

# Bit flags for IS_BTN BStyle
ISB_C1 = 1
ISB_C2 = 2
ISB_C4 = 4
ISB_CLICK = 8
ISB_LIGHT = 16
ISB_DARK = 32
ISB_LEFT = 64
ISB_RIGHT = 128

# Bit flags for BTN CFlags
ISB_LMB = 1
ISB_RMB = 2
ISB_CTRL = 4
ISB_SHIFT = 8

# Enum for IS_RIP Error
RIP_OK = 0
RIP_ALREADY = 1
RIP_DEDICATED = 2
RIP_WRONG_MODE = 3
RIP_NOT_REPLAY = 4
RIP_CORRUPTED = 5
RIP_NOT_FOUND = 6
RIP_UNLOADABLE = 7
RIP_DEST_OOB = 8
RIP_UNKNOWN = 9
RIP_USER = 10
RIP_OOS = 11

# Enum for IS_RIP Options
RIPOPT_LOOP = 1
RIPOPT_SKINS = 2
RIPOPT_FULL_PHYS = 4

# Enum for IS_SSH Error
SSH_OK = 0
SSH_DEDICATED = 1
SSH_CORRUPTED = 2
SSH_NO_SAVE = 3

# Bit flags for IS_NPL SetF
SETF_SYMM_WHEELS = 1
SETF_TC_ENABLE = 2
SETF_ABS_ENABLE = 4


# Languages
LFS_ENGLISH = 0
LFS_DEUTSCH = 1
LFS_PORTUGUESE = 2
LFS_FRENCH = 3
LFS_SUOMI = 4
LFS_NORSK = 5
LFS_NEDERLANDS = 6
LFS_CATALAN = 7
LFS_TURKISH = 8
LFS_CASTELLANO = 9
LFS_ITALIANO = 10
LFS_DANSK = 11
LFS_CZECH = 12
LFS_RUSSIAN = 13
LFS_ESTONIAN = 14
LFS_SERBIAN = 15
LFS_GREEK = 16
LFS_POLSKI = 17
LFS_CROATIAN = 18
LFS_HUNGARIAN = 19
LFS_BRAZILIAN = 20
LFS_SWEDISH = 21
LFS_SLOVAK = 22
LFS_GALEGO = 23
LFS_SLOVENSKI = 24
LFS_BELARUSSIAN = 25
LFS_LATVIAN = 26
LFS_LITHUANIAN = 27
LFS_TRADITIONAL_CHINESE = 28
LFS_SIMPLIFIED_CHINESE = 29
LFS_JAPANESE = 30
LFS_KOREAN = 31
LFS_BULGARIAN = 32
LFS_LATINO = 33
LFS_UKRAINIAN = 34
LFS_INDONESIAN = 35
LFS_ROMANIAN = 36


def _eat_null_chars(str):
    return str.rstrip('\x00')

    
class IS_ISI(object):
    """InSim Init - packet to initialise the InSim system.

    """    
    pack_s = struct.Struct('4B2HBcH15sx15sx')
    def __init__(self, ReqI=0, UDPPort=0, Flags=0, Prefix='\x00', Interval=0, Admin='', IName='pyinsim'):
        """Create a new IS_ISI packet.

        Args:
            ReqI     : If non-zero LFS will send an ``IS_VER`` packet
            UDPPort  : Port for UDP replies from LFS (0 to 65535)
            Flags    : ``ISF_`` bit flags for options
            Prefix   : Special host message prefix character
            Interval : Time in ms between ``IS_NLP`` or ``IS_MCI`` packets (0 = none)
            Admin    : Admin password (if set in LFS)
            IName    : A short name for your program

        """        
        self.Size = 44
        self.Type = ISP_ISI
        self.ReqI = ReqI
        self.Zero = 0
        self.UDPPort = UDPPort
        self.Flags = Flags
        self.Sp0 = 0
        self.Prefix = Prefix
        self.Interval = Interval
        self.Admin = Admin
        self.IName = IName
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.UDPPort, self.Flags, self.Sp0, self.Prefix, self.Interval, self.Admin, self.IName)

class IS_VER(object):
    """VERsion. 

    """    
    pack_s = struct.Struct('4B7sx5sxH')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.Version, self.Product, self.InSimVer = self.pack_s.unpack(data)
        self.Product = _eat_null_chars(self.Product)
        self.Version = _eat_null_chars(self.Version)
        return self

class IS_TINY(object):
    """General purpose packet.

    """    
    pack_s = struct.Struct('4B')
    def __init__(self, ReqI=0, SubT=TINY_NONE):
        """Initialise a new IS_TINY packet.

        Args:
            ReqI : zero (0) unless in response to a request.
            SubT : subtype from ``TINY_*`` enumeration (e.g. ``TINY_REN``)

        """        
        self.Size = 4
        self.Type = ISP_TINY
        self.ReqI = ReqI
        self.SubT = SubT
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.SubT)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.SubT = self.pack_s.unpack(data)
        return self

class IS_SMALL(object):
    """General purpose packet.

    """    
    pack_s = struct.Struct('4BI')
    def __init__(self, ReqI=0, SubT=SMALL_NONE, UVal=0):
        """Initialise a new IS_SMALL packet.

        Args:
            ReqI : zero (0) unless in response to a request.
            SubT : subtype from ``SMALL_*`` enumeration (e.g. ``SMALL_SSP``)
            UVal : value (e.g. for ``SMALL_SSP`` this would be the OutSim packet rate)

        """        
        self.Size = 8
        self.Type = ISP_SMALL
        self.ReqI = ReqI
        self.SubT = SubT
        self.UVal = UVal
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.SubT, self.UVal)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.SubT, self.UVal = self.pack_s.unpack(data)
        return self
    
class IS_STA(object):
    """STAte packet, sent whenever the data in the packet changes. To request
    this packet send a ``IS_TINY`` with a ``ReqI`` of non-zero and a ``SubT`` of ``TINY_STA``.

    """    
    pack_s = struct.Struct('4BfH10B5sx2B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.ReplaySpeed, self.Flags, self.InGameCam, self.ViewPLID, self.NumP, self.NumConns, self.NumFinished, self.RaceInProg, self.QualMins, self.RaceLaps, self.Spare2, self.Spare3, self.Track, self.Weather, self.Wind = self.pack_s.unpack(data)
        self.Track = _eat_null_chars(self.Track)
        return self

class IS_SCH(object):
    """Single CHaracter

    """
    pack_s = struct.Struct('4Bc3B')
    def __init__(self, ReqI=0, CharB='\x00', Flags=0):
        """Initialise a new IS_SCH packet.

        Args:
            ReqI  : 0
            CharB : key to press
            Flags : bit 0 : SHIFT / bit 1 : CTRL

        """
        self.Size = 8
        self.Type = ISP_SCH
        self.ReqI = ReqI
        self.Zero = 0
        self.CharB = CharB
        self.Flags = Flags
        self.Spare2 = 0
        self.Spare3 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.CharB, self.Flags, self.Spare2, self.Spare3)

class IS_SFP(object):
    """State Flags Pack. Send this packet to set the game state. Other states
    must be set by using key-presses or slash commands.

    """
    pack_s = struct.Struct('4BH2B')
    def __init__(self, ReqI=0, Flag=0, OffOn=0):
        """Initialise a new IS_SFP packet.

        Args:
            ReqI  : ReqI as received in the request packet
            Flag  : ``ISS_*`` state flags
            OffOn : 0 = off / 1 = on

        """
        self.Size = 8
        self.Type = ISP_SFP
        self.ReqI = ReqI
        self.Zero = 0
        self.Flag = Flag
        self.OffOn = OffOn
        self.Sp3 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.Flag, self.OffOn, self.Sp3)

class IS_SCC(object):
    """Set Car Camera - Simplified camera packet (not SHIFT+U mode)

    """
    pack_s = struct.Struct('8B')
    def __init__(self, ReqI=0, ViewPLID=0, InGameCam=0):
        """Initialise a new IS_SCC packet.

        Args:
            ReqI      : 0
            ViewPLID  : UniqueID of player to view
            InGameCam : InGameCam (as reported in StatePack)

        """
        self.Size = 8
        self.Type = ISP_SCC
        self.ReqI = ReqI
        self.Zero = 0
        self.ViewPLID = ViewPLID
        self.InGameCam = InGameCam
        self.Sp2 = 0
        self.Sp3 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.ViewPLID, self.InGameCam, self.Sp2, self.Sp3)

class IS_CPP(object):
    """Cam Pos Pack - Full camera packet (in car or SHIFT+U mode)

    """
    pack_s = struct.Struct('4B3i3H2Bf2H')
    def __init__(self, ReqI=0, Pos=[0,0,0], H=0, P=0, R=0, ViewPLID=0, InGameCam=0, FOV=0.0, Time=0, Flags=0):
        """Initialise a new IS_CPP packet.

        Args:
            ReqI      : instruction : 0 / or reply : ReqI as received in the ``TINY_SCP``
            Pos       : Position vector
            H         : heading - 0 points along Y axis
            P         : pitch - 0 means looking at horizon
            R         : roll - 0 means no roll
            ViewPLID  : Unique ID of viewed player (0 = none)
            InGameCam : InGameCam (as reported in StatePack)
            FOV       : FOV in degrees
            Time      : Time to get there (0 means instant + reset)
            Flags     : state flags from ``ISS_*``

        """
        self.Size = 32
        self.Type = ISP_CPP
        self.ReqI = ReqI
        self.Zero = 0
        self.Pos = Pos
        self.H = H
        self.P = P
        self.R = R
        self.ViewPLID = ViewPLID
        self.InGameCam = InGameCam
        self.FOV = FOV
        self.Time = Time
        self.Flags = Flags
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.Pos[0], self.Pos[1], self.Pos[2], self.H, self.P, self.R, self.ViewPLID, self.InGameCam, self.FOV, self.Time, self.Flags)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.Pos[0], self.Pos[1], self.Pos[2], self.H, self.P, self.R, self.ViewPLID, self.InGameCam, self.FOV, self.Time, self.Flags = self.pack_s.unpack(data)
        return self

class IS_ISM(object):
    """InSim Multi

    LFS will send this packet when a host is started or joined.

    """
    pack_s = struct.Struct('8B31sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.Host, self.Sp1, self.Sp2, self.Sp3, self.HName = self.pack_s.unpack(data)
        self.HName = _eat_null_chars(self.HName)
        return self

class IS_MSO(object):
    """MSg Out - system messages and user messages

    """
    pack_s = struct.Struct('8B127sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.UCID, self.PLID, self.UserType, self.TextStart, self.Msg = self.pack_s.unpack(data)
        self.Msg = _eat_null_chars(self.Msg)
        return self

class IS_III(object):
    """InsIm Info - /i message from user to host's InSim

    """
    pack_s = struct.Struct('8B63sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.UCID, self.PLID, self.Sp2, self.Sp3, self.Msg = self.pack_s.unpack(data)
        self.Msg = _eat_null_chars(self.Msg)
        return self

class IS_MST(object):
    """MSg Type - send to LFS to type message or command

    """
    pack_s = struct.Struct('4B63sx')
    def __init__(self, ReqI=0, Msg=''):
        """Initialise a new IS_MST packet.

        Args:
            ReqI : 0
            Msg  : message (64 characters)

        """
        self.Size = 68
        self.Type = ISP_MST
        self.ReqI = ReqI
        self.Zero = 0
        self.Msg = Msg
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.Msg)

class IS_MTC(object):
    """Msg To Connection - hosts only - send to a connection or a player

    """
    pack_s = struct.Struct('8B')
    def __init__(self, ReqI=0, Sound=0, UCID=0, PLID=0, Msg=''):
        """Initialise a new IS_MTC packet.

        Args:
            ReqI : 0
            Sound : the sound to play.
            UCID : connection's unique id (0 = host / 255 = all)
            PLID : player's unique id (if zero, use :attr:`UCID`)
            Msg  : Message (128 characters)

        """
        self.Size = 8
        self.Type = ISP_MTC
        self.ReqI = ReqI
        self.Sound = Sound
        self.UCID = UCID
        self.PLID = PLID
        self.Sp2 = 0
        self.Sp3 = 0
        self.Msg = Msg
    def pack(self):
        TEXT_SIZE = len(self.Msg) + (4 - (len(self.Msg) % 4))
        return self.pack_s.pack(self.Size + TEXT_SIZE, self.Type, self.ReqI, self.Sound, self.UCID, self.PLID, self.Sp2, self.Sp3) + struct.pack('%ds' % TEXT_SIZE, self.Msg)

class IS_MOD(object):
    """MODe : send to LFS to change screen mode

    """
    pack_s = struct.Struct('4B4i')
    def __init__(self, ReqI=0, Bits16=0, RR=0, Width=0, Height=0):
        """Initialise a new IS_MOD packet.

        Args:
            ReqI   : 0
            Bits16 : set to choose 16-bit
            RR     : refresh rate - zero for default
            Width  : 0 means go to window
            Height : 0 means go to window

        """
        self.Size = 20
        self.Type = ISP_MOD
        self.ReqI = ReqI
        self.Zero = 0
        self.Bits16 = Bits16
        self.RR = RR
        self.Width = Width
        self.Height = Height
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.Bits16, self.RR, self.Width, self.Height)

class IS_VTN(object):
    """VoTe Notify

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.UCID, self.Action, self.Spare2, self.Spare3 = self.pack_s.unpack(data)
        return self

class IS_RST(object):
    """Race STart

    """
    pack_s = struct.Struct('8B5sx2B6H')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.RaceLaps, self.QualMins, self.NumP, self.Timing, self.Track, self.Weather, self.Wind, self.Flags, self.NumNodes, self.Finish, self.Split1, self.Split2, self.Split3 = self.pack_s.unpack(data)
        self.Track = _eat_null_chars(self.Track)
        return self

class IS_NCN(object):
    """New ConN

    """
    pack_s = struct.Struct('4B23sx23sx4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.UName, self.PName, self.Admin, self.Total, self.Flags, self.Sp3 = self.pack_s.unpack(data)
        self.UName = _eat_null_chars(self.UName)
        self.PName = _eat_null_chars(self.PName)
        return self

class IS_NCI(object):
    """New Connection Info

    """
    pack_s = struct.Struct('8B2I')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.Language, self.Sp1, self.Sp2, self.Sp3, self.UserID, self.IPAddress = self.pack_s.unpack(data)
        return self

class IS_CNL(object):
    """ConN Leave

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.Reason, self.Total, self.Sp2, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_CPR(object):
    """Conn Player Rename

    """
    pack_s = struct.Struct('4B23sx7sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.PName, self.Plate = self.pack_s.unpack(data)
        self.PName = _eat_null_chars(self.PName)
        #self.Plate = _eat_null_chars(self.Plate) # No trailing zero on Plate.
        return self

class IS_NPL(object):
    """New PLayer joining race (if PLID already exists, then leaving pits)

    """
    pack_s = struct.Struct('6BH23sx8s3sx15sx8Bi4B')
    def unpack(self, data):
        self.Tyres = [0,0,0,0]
        self.Size, self.Type, self.ReqI, self.PLID, self.UCID, self.PType, self.Flags, self.PName, self.Plate, self.CName, self.SName, self.Tyres[0], self.Tyres[1], self.Tyres[2], self.Tyres[3], self.H_Mass, self.H_TRes, self.Model, self.Pass, self.Spare, self.SetF, self.NumP, self.Sp2, self.Sp3 = self.pack_s.unpack(data)
        self.PName = _eat_null_chars(self.PName)
        #self.Plate = _eat_null_chars(self.Plate) # No trailing zero
        self.CName = _eat_null_chars(self.CName)
        self.SName = _eat_null_chars(self.SName)
        return self

class IS_PLP(object):
    """PLayer Pits (go to settings - stays in player list)

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID = self.pack_s.unpack(data)
        return self

class IS_PLL(object):
    """PLayer Leave race (spectate - removed from player list)

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID = self.pack_s.unpack(data)
        return self

class IS_LAP(object):
    """LAP time

    """
    pack_s = struct.Struct('4B2I2H4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.LTime, self.ETime, self.LapsDone, self.Flags, self.Sp0, self.Penalty, self.NumStops, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_SPX(object):
    """SPlit X time

    """
    pack_s = struct.Struct('4B2I4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.STime, self.ETime, self.Split, self.Penalty, self.NumStops, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_PIT(object):
    """PIT stop (stop at pit garage)

    """
    pack_s = struct.Struct('4B2H8B2I')
    def unpack(self, data):
        self.Tyres = [0, 0, 0, 0]
        self.Size, self.Type, self.ReqI, self.PLID, self.LapsDone, self.Flags, self.Sp0, self.Penalty, self.NumStops, self.Sp3, self.Tyres[0], self.Tyres[1], self.Tyres[2], self.Tyres[3], self.Work, self.Spare = self.pack_s.unpack(data)
        return self

class IS_PSF(object):
    """Pit Stop Finished

    """
    pack_s = struct.Struct('4B2I')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.STime, self.Spare = self.pack_s.unpack(data)
        return self

class IS_PLA(object):
    """Pit LAne

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.Fact, self.Sp1, self.Sp2, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_CCH(object):
    """Camera CHange

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.Camera, self.Sp1, self.Sp2, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_PEN(object):
    """PENalty (given or cleared)

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.OldPen, self.NewPen, self.Reason, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_TOC(object):
    """Take Over Car

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.OldUCID, self.NewUCID, self.Sp2, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_FLG(object):
    """FLaG (yellow or blue flag changed)

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.OffOn, self.Flag, self.CarBehind, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_PFL(object):
    """Player FLags (help flags changed)

    """
    pack_s = struct.Struct('4B2H')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.Flags, self.Spare = self.pack_s.unpack(data)
        return self

class IS_FIN(object):
    """FINished race notification (not a final result - use :class:`IS_RES`)

    """
    pack_s = struct.Struct('4B2I4B2H')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.TTime, self.BTime, self.SpA, self.NumStops, self.Confirm, self.SpB, self.LapsDone, self.Flags = self.pack_s.unpack(data)
        return self

class IS_RES(object):
    """RESult (qualify or confirmed finish)

    """
    pack_s = struct.Struct('4B23sx23sx7sx3sx2I4B2H2BH')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID, self.UName, self.PName, self.Plate, self.CName, self.TTime, self.BTime, self.SpA, self.NumStops, self.Confirm, self.SpB, self.LapsDone, self.Flags, self.ResultNum, self.NumRes, self.PSeconds = self.pack_s.unpack(data)
        self.UName = _eat_null_chars(self.UName)
        self.PName = _eat_null_chars(self.PName)
        self.Plate = _eat_null_chars(self.Plate) # No trailing zero
        self.CName = _eat_null_chars(self.CName)
        return self

class IS_REO(object):
    """REOrder (when race restarts after qualifying). The NumP value
    is filled in automatically from the PLID length.

    """
    pack_s = struct.Struct('4B')
    def __init__(self, ReqI=0, PLID=[]):
        """Initialise a new IS_REO packet. 

        Args:
            ReqI : 0 unless this is a reply to an ``TINY_REO`` request
            PLID : all PLIDs in new order

        """
        self.Size = 4 + MAX_PLAYERS
        self.Type = ISP_REO
        self.ReqI = ReqI
        self.NumP = len(PLID)
        self.PLID = PLID
    def pack(self):
        plid = ''.join([chr(p) for p in self.PLID]).ljust(MAX_PLAYERS, '\x00')
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, len(self.PLID)) + plid
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.NumP = self.pack_s.unpack(data[:4])
        self.PLID = [ord(data[4+i]) for i in xrange(self.NumP)]
        return self

class IS_NLP(object):
    """Node and Lap Packet - variable size

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.NumP = self.pack_s.unpack(data[:4])
        data = data[4:]
        self.Info = [NodeLap(data, i) for i in xrange(0, self.NumP * 6, 6)]
        return self

class NodeLap(object):
    """Car info in 6 bytes - there is an array of these in the :class:`IS_NLP`

    """
    pack_s = struct.Struct('2H2B')
    def __init__(self, data, index):
        """Initialise a new NodeLap sub-packet.

        """
        self.Node, self.Lap, self.PLID, self.Position = self.pack_s.unpack(data[index:index+6])

class IS_MCI(object):
    """Multi Car Info - if more than 8 in race then more than one of these is sent

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.NumC = self.pack_s.unpack(data[:4])
        data = data[4:]
        self.Info = [CompCar(data, i) for i in xrange(0, self.NumC * 28, 28)]
        return self

class CompCar(object):
    """Car info in 28 bytes - there is an array of these in the :class:`IS_MCI`

    """
    pack_s = struct.Struct('2H4B3i3Hh')
    def __init__(self, data, index):
        """Initialise a new CompCar sub-packet.

        """
        self.Node, self.Lap, self.PLID, self.Position, self.Info, self.Sp3, self.X, self.Y, self.Z, self.Speed, self.Direction, self.Heading, self.AngVel = self.pack_s.unpack(data[index:index+28])
        
class IS_MSX(object):
    """MSg eXtended - like ``IS_MST`` but longer (not for commands)

    """
    pack_s = struct.Struct('4B95sx')
    def __init__(self, ReqI=0, Msg=''):
        """Initialise a new IS_MSX packet.

        Args:
            ReqI : 0
            Msg  : last byte must be zero
        
        """
        self.Size = 100
        self.Type = ISP_MSX
        self.ReqI = ReqI
        self.Zero = 0
        self.Msg = Msg
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.Msg)

class IS_MSL(object):
    """MSg Local - message to appear on local computer only

    """
    pack_s = struct.Struct('4B127sx')
    def __init__(self, ReqI=0, Sound=0, Msg=''):
        """Initialise a new IS_MSL packet.

        Args:
            ReqI  : 0
            Sound : Sound from ``SND_*`` enumeration.
            Msg   : Message

        """
        self.Size = 132
        self.Type = ISP_MSL
        self.ReqI = ReqI
        self.Sound = Sound
        self.Msg = Msg
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Sound, self.Msg)

class IS_CRS(object):
    """Car ReSet

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID = self.pack_s.unpack(data)
        return self

class IS_BFN(object):
    """Button FunctioN - delete buttons / receive button requests

    """
    pack_s = struct.Struct('8B')
    def __init__(self, ReqI=0, SubT=0, UCID=0, ClickID=0, Inst=0):
        """Initialise a new IS_BFN packet.

        Args:
            ReqI    : 0
            SubT    : subtype, from ``BFN_*`` enumeration
            UCID    : connection to send to or from (0 = local / 255 = all)
            ClickID : ID of button to delete (if ``SubT`` is ``BFN_DEL_BTN``)
            Inst    : used internally by InSim

        """
        self.Size = 8
        self.Type = ISP_BFN
        self.ReqI = ReqI
        self.SubT = SubT
        self.UCID = UCID
        self.ClickID = ClickID
        self.Inst = Inst
        self.Sp3 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.SubT, self.UCID, self.ClickID, self.Inst, self.Sp3)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.SubT, self.UCID, self.ClickID, self.Inst, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_AXI(object):
    """AutoX Info

    """
    pack_s = struct.Struct('6BH31sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.AXStart, self.NumCP, self.NumO, self.LName = self.pack_s.unpack(data)
        self.LName = _eat_null_chars(self.LName)
        return self

class IS_AXO(object):
    """AutoX Object

    """
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.PLID = self.pack_s.unpack(data)
        return self

class IS_BTN(object):
    """BuTtoN - button header - followed by 0 to 240 characters

    """
    pack_s = struct.Struct('12B')
    def __init__(self, ReqI=0, UCID=0, ClickID=0, Inst=0, BStyle=0, TypeIn=0, L=0, T=0, W=0, H=0, Text=''):
        """Initialise a new IS_BTN packet.

        Args:
            ReqI    : non-zero (returned in ``IS_BTC`` and ``IS_BTT`` packets)
            UCID    : connection to display the button (0 = local / 255 = all)
            ClickID : button ID (0 to 239)
            Inst    : some extra flags from ``INST_*``
            BStyl   : button style flags from ``ISB_*``
            TypeIn  : max chars to type in
            L       : left: 0 - 200
            T       : top: 0 - 200
            W       : width: 0 - 200
            H       : height: 0 - 200
            Text    : 0 to 240 characters of text

        """
        self.Size = 12
        self.Type = ISP_BTN
        self.ReqI = ReqI
        self.UCID = UCID
        self.ClickID = ClickID
        self.Inst = Inst
        self.BStyle = BStyle
        self.TypeIn = TypeIn
        self.L = L
        self.T = T
        self.W = W
        self.H = H
        self.Text = Text
    def pack(self):
        TEXT_SIZE = int(math.ceil(len(self.Text) / 4.0)) * 4
        return self.pack_s.pack(self.Size + TEXT_SIZE, self.Type, self.ReqI, self.UCID, self.ClickID, self.Inst, self.BStyle, self.TypeIn, self.L, self.T, self.W, self.H) + struct.pack('%ds' % TEXT_SIZE, self.Text)

class IS_BTC(object):
    """BuTton Click - sent back when user clicks a button

    """
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.ClickID, self.Inst, self.CFlags, self.Sp3 = self.pack_s.unpack(data)
        return self

class IS_BTT(object):
    """BuTton Type - sent back when user types into a text entry button

    """
    pack_s = struct.Struct('8B95sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.UCID, self.ClickID, self.Inst, self.TypeIn, self.Sp3, self.Text = self.pack_s.unpack(data)
        self.Text = _eat_null_chars(self.Text)
        return self

class IS_RIP(object):
    """Replay Information Packet

    """
    pack_s = struct.Struct('8B2H63sx')
    def __init__(self, ReqI=0, Error=0, MPR=0, Paused=0, Options=0, CTime=0, TTime=0, RName=''):
        """Initialise a new IS_RIP packet.

        Args:
            ReqI    : request : non-zero / reply : same value returned
            Error   : 0 or 1 = OK / options from ``RIP_*``
            MPR     : 0 = SPR / 1 = MPR
            Paused  : request : pause on arrival / reply : paused state
            Options : various options from ``RIPOPT_*``
            CTime   : (hundredths) request : destination / reply : position
            TTime   : (hundredths) request : zero / reply : replay length
            RName   : zero or replay name: last byte must be zero

        """
        self.Size = 76
        self.Type = ISP_RIP
        self.ReqI = ReqI
        self.Error = Error
        self.MPR = MPR
        self.Paused = Paused
        self.Options = Options
        self.Sp3 = 0
        self.CTime = CTime
        self.TTime = TTime
        self.RName = RName
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Error, self.MPR, self.Paused, self.Options, self.Sp3, self.CTime, self.TTime, self.RName)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Error, self.MPR, self.Paused, self.Options, self.Sp3, self.CTime, self.TTime, self.RName = self.pack_s.unpack(data)
        self.RName = _eat_null_chars(self.RName)
        return self

class IS_SSH(object):
    """ScreenSHot

    """
    pack_s = struct.Struct('8B31sx')
    def __init__(self, ReqI=0, Error=0, BMP=''):
        """Initialise a new IS_SSH packet.

        Args:
            ReqI  : request : non-zero / reply : same value returned
            Error : 0 = OK / other values from ``SSH_*``
            BMP   : name of screenshot file: last byte must be zero

        """
        self.Size = 40
        self.Type = ISP_SSH
        self.ReqI = ReqI
        self.Error = Error
        self.Sp0 = 0
        self.Sp1 = 0
        self.Sp2 = 0
        self.Sp3 = 0
        self.BMP = BMP
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Error, self.Sp0, self.Sp1, self.Sp2, self.Sp3, self.BMP)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Error, self.Sp0, self.Sp1, self.Sp2, self.Sp3, self.BMP = self.pack_s.unpack(data)
        self.BMP = _eat_null_chars(self.BMP)
        return self 
    
class CarContact(object):
    """Info about one car in a contact - two of these in the IS_CON
        
    """
    pack_s = struct.Struct('3Bb6b2B2h')
    def __init__(self, data):
        self.PLID, self.Info, self.Sp2, self.Steer, self.ThrBrk, self.CluHan, self.GearSp, self.Speed, self.Direction, self.Heading, self.AccelF, self.AccelR, self.X, self.Y = self.pack_s.unpack(data)
    
class IS_CON(object):
    """CONtact - between two cars (A and B are sorted by PLID)
    
    """
    pack_s = struct.Struct('4B2H')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.SpClose, self.Time = self.pack_s.unpack(data[:8])
        self.A = CarContact(data[8:24])
        self.B = CarContact(data[24:])
        return self
        
class CarContOBJ(object):
    def __init__(self):
        self.Direction = 0
        self.Heading = 0
        self.Speed = 0
        self.Sp2 = 0
        self.X = 0      
        self.Y = 0

OBH_LAYOUT = 1 
OBH_CAN_MOVE = 2      
OBH_WAS_MOVING = 4       
OBH_ON_SPOT = 8

class IS_OBH(object):
    pack_s = struct.Struct('4B2H4B2h2h4B')
    def unpack(self, data):
        self.C = CarContOBJ()
        self.Size, self.Type, self.ReqI, self.PLID, self.SpClose, self.Time, self.C.Direction, self.C.Heading, self.C.Speed, self.C.Sp2, self.C.X, self.C.Y, self.X, self.Y, self.Sp0, self.Sp1, self.Index, self.OBHFlags = self.pack_s.unpack(data)
        return self
    
class IS_HLV(object):
    pack_s = struct.Struct('6BH4B2h')
    def unpack(self, data):
        self.C = CarContOBJ()
        self.Size, self.Type, self.ReqI, self.PLID, self.HLVC, self.Sp1, self.Time, self.C.Direction, self.C.Heading, self.C.Speed, self.C.Sp2, self.C.X, self.C.Y = self.pack_s.unpack(data)
        return self
    
class ObjectInfo(object):
    pack_s = struct.Struct('2h4B')
    def __init__(self, data, index):
        self.X, self.Y, self.Zbyte, self.Flags, self.Index, self.Heading = self.pack_s.unpack(data[index:index+8])
        
PMO_LOADING_FILE = 0,
PMO_ADD_OBJECTS = 1, 
PMO_DEL_OBJECTS = 2,
PMO_CLEAR_ALL = 3,
        
class IS_AXM(object):
    pack_s = struct.Struct('8B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.NumO, self.UCID, self.PMOAction, self.PMOFlags, self.Sp3 = self.pack_s.unpack(data[:8])
        data = data[8:]
        self.Info = [ObjectInfo(data, i) for i in xrange(0, self.NumO * 8, 8)]
        return self

class IS_ACR(object):
    pack_s = struct.Struct('8B63sx')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Zero, self.UCID, self.Admin, self.Result, self.Sp3, self.Text = self.pack_s.unpack(data)
        self.Text = _eat_null_chars(self.Text)
        return self

CAR_NONE = 0
CAR_XFG = 1
CAR_XRG = 2
CAR_XRT = 4
CAR_RB4 = 8
CAR_FXO = 0x10
CAR_LX4 = 0x20
CAR_LX6 = 0x40
CAR_MRT = 0x80
CAR_UF1 = 0x100
CAR_RAC = 0x200
CAR_FZ5 = 0x400
CAR_FOX = 0x800
CAR_XFR = 0x1000
CAR_UFR = 0x2000
CAR_FO8 = 0x4000
CAR_FXR = 0x8000
CAR_XRR = 0x10000
CAR_FZR = 0x20000
CAR_BF1 = 0x40000
CAR_FBM = 0x80000
CAR_ALL = 0xffffffff

class IS_PLC(object):
    pack_s = struct.Struct('8BI')
    def __init__(self, UCID=0, Cars=CAR_NONE):
        self.Size = 12
        self.Type = ISP_PLC
        self.ReqI = 0
        self.Zero = 0
        self.UCID = UCID
        self.Sp1 = 0
        self.Sp2 = 0
        self.Sp3 = 0
        self.Cars = Cars
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.UCID, self.Sp1, self.Sp2, self.Sp3, self.Cars)

    
# InSim Relay

# Host flags
HOS_SPECPASS = 1
HOS_LICENSED = 2
HOS_S1       = 4
HOS_S2       = 8
HOS_FIRST    = 64
HOS_LAST     = 128

IR_ERR_PACKET   = 1
IR_ERR_PACKET2  = 2
IR_ERR_HOSTNAME = 3
IR_ERR_ADMIN    = 4
IR_ERR_SPEC     = 5
IR_ERR_NOSPEC   = 6

class IR_HLR(object):
    pack_s = struct.Struct('4B')
    def __init__(self, ReqI=0):
        self.Size = 4
        self.Type = IRP_HLR
        self.ReqI = ReqI
        self.Sp0 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Sp0)

class IR_HOS(object):
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.NumHosts = self.pack_s.unpack(data[:4])
        data = data[4:]
        self.Info = [HInfo(data, i) for i in xrange(0, self.NumHosts * 40, 40)]  
        return self
            
class HInfo(object):
    pack_s = struct.Struct('31sx5sx2B')
    def __init__(self, data, index):
        self.HName, self.Track, self.Flags, self.NumConns = self.pack_s.unpack(data[index:index+40])   
        self.HName = _eat_null_chars(self.HName)
        self.Track = _eat_null_chars(self.Track)
        
class IR_SEL(object):
    pack_s = struct.Struct('4B31sx15sx15sx')
    def __init__(self, ReqI=0, HName='', Admin='', Spec=''):
        self.Size = 68
        self.Type = IRP_SEL
        self.ReqI = ReqI
        self.Zero = 0
        self.HName = HName
        self.Admin = Admin
        self.Spec = Spec
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Zero, self.HName, self.Admin, self.Spec)
        
class IR_ARQ(object):
    pack_s = struct.Struct('4B')
    def __init__(self, ReqI=0):
        self.Size = 4
        self.Type = IRP_ARQ
        self.ReqI = ReqI
        self.Sp0 = 0
    def pack(self):
        return self.pack_s.pack(self.Size, self.Type, self.ReqI, self.Sp0)

class IR_ARP(object):
    pack_s = struct.Struct('4B')
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.Admin = self.pack_s.unpack(data)
        return self
      
class IR_ERR(object):
    pack_s = struct.Struct('4B'
)
    def unpack(self, data):
        self.Size, self.Type, self.ReqI, self.ErrNo = self.pack_s.unpack(data)
        return self
        
class OutSimPack(object):
    pack_s = struct.Struct('I12f3i')
    def __init__(self):
        self.Time = 0
        self.AngVel = [0.0, 0.0, 0.0]
        self.Heading = 0.0
        self.Pitch = 0.0
        self.Roll = 0.0
        self.Accel = [0.0, 0.0, 0.0]
        self.Vel = [0.0, 0.0, 0.0]
        self.Pos = [0, 0, 0]
        self.ID = 0
    def unpack(self, data):
        self.Time, self.AngVel[0], self.AngVel[1], self.AngVel[2], self.Heading, self.Pitch, self.Roll, self.Accel[0], self.Accel[1], self.Accel[2], self.Vel[0], self.Vel[1], self.Vel[2], self.Pos[0], self.Pos[1], self.Pos[2] = self.pack_s.unpack(data[:64])
        if len(data) == 68:
            self.ID = struct.unpack('i', data[64:])
        return self
             
# Bits for OutGaugePack Flags
OG_SHIFT = 1
OG_CTRL = 2
OG_TURBO = 8192
OG_KM = 16384
OG_BAR = 32768

# Bits for OutGaugePack DashLights and ShowLights
DL_SHIFT = 1
DL_FULLBEAM = 2
DL_HANDBRAKE = 4
DL_PITSPEED = 8
DL_TC = 16
DL_SIGNAL_L = 32
DL_SIGNAL_R = 64
DL_SIGNAL_ANY = 128
DL_OILWARN = 256
DL_BATTERY = 512
DL_ABS = 1024
DL_SPARE = 2048
DL_NUM= 4096             
                    
class OutGaugePack(object):
    pack_s = struct.Struct('I3sxH2B7f2I3f15sx15sx')
    def __init__(self):      
        self.Time = 0
        self.Car = ''
        self.Flags = 0
        self.Gear = 0
        self.PLID = 0
        self.Speed = 0.0
        self.RPM = 0.0
        self.Turbo = 0.0
        self.EngTemp = 0.0
        self.Fuel = 0.0
        self.OilPress = 0.0
        self.OilTemp = 0.0
        self.DashLights = 0
        self.ShowLights = 0
        self.Throttle = 0.0
        self.Brake = 0.0
        self.Clutch = 0.0
        self.Display1 = ''
        self.Display2 = ''
        self.ID = 0
    def unpack(self, data):
        self.Time, self.Car, self.Flags, self.Gear, self.PLID, self.Speed, self.RPM, self.Turbo, self.EngTemp,self.Fuel, self.OilPress, self.OilTemp, self.DashLights, self.ShowLights, self.Throttle, self.Brake, self.Clutch, self.Display1,self.Display2 = self.pack_s.unpack(data[:92])
        self.Display1 = _eat_null_chars(self.Display1)
        self.Display2 = _eat_null_chars(self.Display2)
        if len(data) == 96:
            self.ID = struct.unpack('i', data[92:])
        return self
               
               
if __name__ == '__main__':
    pass
    #print [d for d in dir() if not d.startswith('_') and d not in ('struct', 'math')]
        