from ctypes import c_int32
from pathlib import Path

APP_DIR = Path("C:/Users/usuario/Desktop/Álvaro/Uni/TFG/AC-Telemetry")

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
            {"name": "packetId", "description": "Packet ID of the current graphical step"},
            {"name": "status", "description": "Status of the Assetto Corsa instance"},
            {"name": "session", "description": "Type of the current session"},
            {"name": "currentTime", "description": "Current lap time"},
            {"name": "lastTime", "description": "Last lap time"},
            {"name": "bestTime", "description": "Best lap time"},
            {"name": "split", "description": "Time in the current sector"},
            {"name": "completedLaps", "description": "Number of laps completed by the player"},
            {"name": "position", "description": "Current position of the player in the standings"},
            {"name": "iCurrentTime", "description": "Current lap time in integer format"},
            {"name": "iLastTime", "description": "Last lap time in integer format"},
            {"name": "iBestTime", "description": "Best lap time in integer format"},
            {"name": "sessionTimeLeft", "description": "Time remaining in the session"},
            {"name": "distanceTraveled", "description": "Total distance traveled by the player"},
            {"name": "isInPit", "description": "Indicates if the player's car is stopped in the pit (0: No, 1: Yes)"},
            {"name": "currentSectorIndex", "description": "Current sector index of the track"},
            {"name": "lastSectorTime", "description": "Time taken in the last sector"},
            {"name": "numberOfLaps", "description": "Total number of laps required to complete the session"},
            {"name": "tyreCompound", "description": "Current tyre compound being used"},
            {"name": "replayTimeMultiplier", "description": "Multiplier for replay speed"},
            {"name": "normalizedCarPosition", "description": "Position of the car on the track's spline (0-1)"},
            {"name": "carCoordinates", "description": "Coordinates of the car in the world (x, y, z)"},
            {"name": "penaltyTime", "description": "Time penalty for the player"},
            {"name": "flag", "description": "Current flag status (e.g., blue, yellow, black)"},
            {"name": "idealLineOn", "description": "Indicates if the ideal line is enabled (0: No, 1: Yes)"},
            {"name": "isInPitLane", "description": "Indicates if the player's car is in the pitlane (0: No, 1: Yes)"},
            {"name": "surfaceGrip", "description": "Current grip level of the track surface"},
            {"name": "mandatoryPitDone", "description": "Indicates if the mandatory pit stop is completed (0: No, 1: Yes)"},
            {"name": "windSpeed", "description": "Speed of the wind in the current session"},
            {"name": "windDirection", "description": "Direction of the wind in degrees (0-359)"}
        ]
    },
    "physics_info": {
        "variables": [
            {"name": "packetId", "description": "Packet ID of the current physics step"},
            {"name": "gas", "description": "Gas pedal position (0: Not pressed, 1: Fully pressed)"},
            {"name": "brake", "description": "Brake pedal position (0: Not pressed, 1: Fully pressed)"},
            {"name": "fuel", "description": "Amount of fuel in the car (liters)"},
            {"name": "gear", "description": "Selected gear (0: Reverse, 1: Neutral, 2: First gear)"},
            {"name": "rpms", "description": "Engine revolutions per minute (RPM)"},
            {"name": "steerAngle", "description": "Steering angle"},
            {"name": "speedKmh", "description": "Speed in kilometers per hour (km/h)"},
            {"name": "velocity", "description": "Velocity vector for each axis (world coordinates) [x, y, z]"},
            {"name": "accG", "description": "G-force for each axis (local coordinates) [x, y, z]"},
            {"name": "wheelSlip", "description": "Spin speed of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "wheelLoad", "description": "Load on each tire (in Newtons) [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "wheelsPressure", "description": "Pressure of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "wheelAngularSpeed", "description": "Angular speed of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreWear", "description": "Current wear level of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreDirtyLevel", "description": "Dirt level on each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreCoreTemperature", "description": "Core temperature of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "camberRAD", "description": "Camber angle of each tire in radians [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "suspensionTravel", "description": "Suspension travel for each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "drs", "description": "DRS status (0: Disabled, 1: Enabled)"},
            {"name": "tc", "description": "Traction control slip ratio limit (if enabled)"},
            {"name": "heading", "description": "Heading angle of the car (world coordinates)"},
            {"name": "pitch", "description": "Pitch angle of the car (world coordinates)"},
            {"name": "roll", "description": "Roll angle of the car (world coordinates)"},
            {"name": "cgHeight", "description": "Height of the car's center of gravity"},
            {"name": "carDamage", "description": "Damage level for each car section (only first 4 are valid)"},
            {"name": "numberOfTyresOut", "description": "Number of tires allowed out of track before receiving a penalty"},
            {"name": "pitLimiterOn", "description": "Pit limiter status (0: Disabled, 1: Enabled)"},
            {"name": "abs", "description": "ABS slip ratio limit (if enabled)"},
            {"name": "kersCharge", "description": "KERS/ERS battery charge level (0: Empty, 1: Full)"},
            {"name": "kersInput", "description": "KERS/ERS input to the engine (0: None, 1: Maximum)"},
            {"name": "autoShifterOn", "description": "Automatic shifter status (0: Disabled, 1: Enabled)"},
            {"name": "rideHeight", "description": "Ride height at the front and rear"},
            {"name": "turboBoost", "description": "Turbo boost level"},
            {"name": "ballast", "description": "Additional ballast weight added to the car (multiplayer only)"},
            {"name": "airDensity", "description": "Air density"},
            {"name": "airTemp", "description": "Ambient air temperature"},
            {"name": "roadTemp", "description": "Track surface temperature"},
            {"name": "localAngularVel", "description": "Angular velocity of the car [x, y, z]"},
            {"name": "finalFF", "description": "Current force feedback value"},
            {"name": "performanceMeter", "description": "Performance meter compared to the best lap"},
            {"name": "engineBrake", "description": "Engine brake setting"},
            {"name": "ersRecoveryLevel", "description": "ERS recovery level"},
            {"name": "ersPowerLevel", "description": "ERS power controller setting"},
            {"name": "ersHeatCharging", "description": "ERS heat charging status (0: Motor, 1: Battery)"},
            {"name": "ersIsCharging", "description": "ERS battery charging status (0: Not charging, 1: Charging)"},
            {"name": "kersCurrentKJ", "description": "KERS/ERS energy spent during the lap (in Kilojoules)"},
            {"name": "drsAvailable", "description": "DRS availability (0: Not available, 1: Available)"},
            {"name": "drsEnabled", "description": "DRS enabled status (0: Disabled, 1: Enabled)"},
            {"name": "brakeTemp", "description": "Brake temperature for each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "clutch", "description": "Clutch pedal position (0: Not pressed, 1: Fully pressed)"},
            {"name": "tyreTempI", "description": "Inner temperature of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreTempM", "description": "Middle temperature of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreTempO", "description": "Outer temperature of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "isAIControlled", "description": "AI control status (0: Human, 1: AI)"},
            {"name": "tyreContactPoint", "description": "Contact point vector for each tire [Front Left, Front Right, Rear Left, Rear Right][x, y, z]"},
            {"name": "tyreContactNormal", "description": "Contact normal vector for each tire [Front Left, Front Right, Rear Left, Rear Right][x, y, z]"},
            {"name": "tyreContactHeading", "description": "Contact heading vector for each tire [Front Left, Front Right, Rear Left, Rear Right][x, y, z]"},
            {"name": "brakeBias", "description": "Brake bias (0: Rear, 1: Front)"},
            {"name": "localVelocity", "description": "Local velocity vector [x, y, z]"}
        ]
    },
    "static_info": {
        "variables": [
            {"name": "_smVersion", "description": "Version of the shared memory structure"},
            {"name": "_acVersion", "description": "Version of Assetto Corsa"},
            {"name": "numberOfSessions", "description": "Total number of sessions in this instance"},
            {"name": "numCars", "description": "Maximum number of cars on track"},
            {"name": "carModel", "description": "Name of the player's car model"},
            {"name": "track", "description": "Name of the track"},
            {"name": "playerName", "description": "First name of the player"},
            {"name": "playerSurname", "description": "Surname of the player"},
            {"name": "playerNick", "description": "Nickname of the player"},
            {"name": "sectorCount", "description": "Number of track sectors"},
            {"name": "maxTorque", "description": "Maximum torque value of the player's car"},
            {"name": "maxPower", "description": "Maximum power value of the player's car"},
            {"name": "maxRpm", "description": "Maximum RPM value of the player's car"},
            {"name": "maxFuel", "description": "Maximum fuel capacity of the player's car"},
            {"name": "suspensionMaxTravel", "description": "Maximum suspension travel distance of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "tyreRadius", "description": "Radius of each tire [Front Left, Front Right, Rear Left, Rear Right]"},
            {"name": "maxTurboBoost", "description": "Maximum turbo boost value of the player's car"},
            {"name": "deprecated_1", "description": "Deprecated field (do not use)"},
            {"name": "deprecated_2", "description": "Deprecated field (do not use)"},
            {"name": "penaltiesEnabled", "description": "Cut penalties enabled (1: True, 0: False)"},
            {"name": "aidFuelRate", "description": "Fuel consumption rate (0: No consumption, 1: Normal, 2: Double consumption)"},
            {"name": "aidTireRate", "description": "Tire wear rate (0: No wear, 1: Normal, 2: Double wear)"},
            {"name": "aidMechanicalDamage", "description": "Mechanical damage rate (0: No damage, 1: Normal)"},
            {"name": "aidAllowTyreBlankets", "description": "Tire blankets aid enabled (1: True, 0: False)"},
            {"name": "aidStability", "description": "Stability aid level (0: No aid, 1: Full aid)"},
            {"name": "aidAutoClutch", "description": "Automatic clutch enabled (1: True, 0: False)"},
            {"name": "aidAutoBlip", "description": "Automatic blip enabled (1: True, 0: False)"},
            {"name": "hasDRS", "description": "DRS system equipped (1: Yes, 0: No)"},
            {"name": "hasERS", "description": "ERS system equipped (1: Yes, 0: No)"},
            {"name": "hasKERS", "description": "KERS system equipped (1: Yes, 0: No)"},
            {"name": "kersMaxJ", "description": "Maximum KERS Joule value"},
            {"name": "engineBrakeSettingsCount", "description": "Number of engine brake settings"},
            {"name": "ersPowerControllerCount", "description": "Number of ERS power controller settings"},
            {"name": "trackSPlineLength", "description": "Length of the track spline"},
            {"name": "trackConfiguration", "description": "Name of the track configuration (only for multi-layout tracks)"},
            {"name": "ersMaxJ", "description": "Maximum ERS Joule value"},
            {"name": "isTimedRace", "description": "Timed race status (1: Yes, 0: No)"},
            {"name": "hasExtraLap", "description": "Extra lap included in timed race (1: Yes, 0: No)"},
            {"name": "carSkin", "description": "Name of the car skin being used"},
            {"name": "reversedGridPositions", "description": "Number of positions swapped in the second race"},
            {"name": "PitWindowStart", "description": "Start of the pit window (Lap/Minute)"},
            {"name": "PitWindowEnd", "description": "End of the pit window (Lap/Minute)"}
        ]
    }
}

