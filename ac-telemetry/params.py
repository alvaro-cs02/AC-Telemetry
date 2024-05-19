
from ctypes import c_int32
from pathlib import Path

AC_APP_DIR = Path("D:/Work/projects/AC-Telemetry/ac-telemetry")

APP_DIR = Path("D:/path/to/your/telemetry/extractor/project")

LOG_DIR = APP_DIR / "logs"
CONFIG_FILE = APP_DIR / "config.json"
AC_STATUS = c_int32
AC_OFF = 0
AC_REPLAY = 1
AC_LIVE = 2
AC_PAUSE = 3

AC_SESSION_TYPE = c_int32
AC_UNKNOWN = -1
AC_PRACTICE = 0
AC_QUALIFY = 1
AC_RACE = 2
AC_HOTLAP = 3
AC_TIME_ATTACK = 4
AC_DRIFT = 5
AC_DRAG = 6

AC_FLAG_TYPE = c_int32
AC_NO_FLAG = 0
AC_BLUE_FLAG = 1
AC_YELLOW_FLAG = 2
AC_BLACK_FLAG = 3
AC_WHITE_FLAG = 4
AC_CHECKERED_FLAG = 5
AC_PENALTY_FLAG = 6