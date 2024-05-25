from ctypes import c_int32
from pathlib import Path

APP_DIR = Path("D:/Work/projects/AC-Telemetry")

LOG_DIR = APP_DIR / "logs"
CONFIG_FILE = APP_DIR / "app/commons/config.yaml"
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

TELEMETRY_VARIABLES = {
    "graphic_info": {
        "variables": [
            {"name": "carCoordinates", "description": "The car's coordinates"},
            {"name": "penalty", "description": "Current penalty status"},
            {"name": "flag", "description": "Current flag status"},
        ]
    },
    "physics_info": {
        "variables": [
            {"name": "rpms", "description": "Engine revolutions per minute"},
            {"name": "speedKmh", "description": "Speed in kilometers per hour"},
            {"name": "gear", "description": "Current gear"},
        ]
    },
    "static_info": {
        "variables": [
            {"name": "maxRpm", "description": "Maximum RPM"},
            {"name": "maxFuel", "description": "Maximum fuel capacity"},
            {"name": "suspensionMaxTravel", "description": "Maximum suspension travel"},
        ]
    }
}
