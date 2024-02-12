import mmap
import functools
import ctypes
import time
from datetime import datetime
import pandas as pd
import json
from ctypes import c_int32, c_float, c_wchar


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

class SPageFilePhysics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('packetId', c_int32),
        ('gas', c_float),
        ('brake', c_float),
        ('fuel', c_float),
        ('gear', c_int32),
        ('rpms', c_int32),
        ('steerAngle', c_float),
        ('speedKmh', c_float),
        ('velocity', c_float * 3),
        ('accG', c_float * 3),
        ('wheelSlip', c_float * 4),
        ('wheelLoad', c_float * 4),
        ('wheelsPressure', c_float * 4),
        ('wheelAngularSpeed', c_float * 4),
        ('tyreWear', c_float * 4),
        ('tyreDirtyLevel', c_float * 4),
        ('tyreCoreTemperature', c_float * 4),
        ('camberRAD', c_float * 4),
        ('suspensionTravel', c_float * 4),
        ('drs', c_float),
        ('tc', c_float),
        ('heading', c_float),
        ('pitch', c_float),
        ('roll', c_float),
        ('cgHeight', c_float),
        ('carDamage', c_float * 5),
        ('numberOfTyresOut', c_int32),
        ('pitLimiterOn', c_int32),
        ('abs', c_float),
        ('kersCharge', c_float),
        ('kersInput', c_float),
        ('autoShifterOn', c_int32),
        ('rideHeight', c_float*2),
        ('turboBoost', c_float),
        ('ballast', c_float),
        ('airDensity', c_float),
        ('airTemp', c_float),
        ('roadTemp', c_float),
        ('localAngularVel', c_float*3),
        ('finalFF', c_float),
        ('performanceMeter', c_float),
        ('engineBrake', c_int32),
        ('ersRecoveryLevel', c_int32),
        ('ersPowerLevel', c_int32),
        ('ersHeatCharging', c_int32),
        ('ersIsCharging', c_int32),
        ('kersCurrentKJ', c_float),
        ('drsAvailable', c_int32),
        ('drsEnabled', c_int32),
        ('brakeTemp', c_float*4),
        ('clutch', c_float),
        ('tyreTempI', c_float*4),
        ('tyreTempM', c_float*4),
        ('tyreTempO', c_float*4),
        ('isAIControlled', c_int32),
        ('tyreContactPoint', c_float*4*3),
        ('tyreContactNormal', c_float*4*3),
        ('tyreContactHeading', c_float*3*4),
        ('brakeBias', c_float),
        ('localVelocity', c_float*3),
        ('P2PActivation', c_int32),
        ('P2PStatus', c_int32),
        ('currentMaxRpm', c_float),
    ]


class SPageFileGraphic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('packetId', c_int32),
        ('status', AC_STATUS),
        ('session', AC_SESSION_TYPE),
        ('currentTime', c_wchar * 15),
        ('lastTime', c_wchar * 15),
        ('bestTime', c_wchar * 15),
        ('split', c_wchar * 15),
        ('completedLaps', c_int32),
        ('position', c_int32),
        ('iCurrentTime', c_int32),
        ('iLastTime', c_int32),
        ('iBestTime', c_int32),
        ('sessionTimeLeft', c_float),
        ('distanceTraveled', c_float),
        ('isInPit', c_int32),
        ('currentSectorIndex', c_int32),
        ('lastSectorTime', c_int32),
        ('numberOfLaps', c_int32),
        ('tyreCompound', c_wchar * 33),
        ('replayTimeMultiplier', c_float),
        ('normalizedCarPosition', c_float),
        ('carCoordinates', c_float * 3),
        ('penaltyTime', c_float),
        ('flag', AC_FLAG_TYPE),
        ('idealLineOn', c_int32),
        ('isInPitLane', c_int32),
        ('surfaceGrip', c_float),
        ('mandatoryPitDone', c_int32),
        ('windSpeed', c_float),
        ('windDirection', c_float)
    ]


class SPageFileStatic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('_smVersion', c_wchar * 15),
        ('_acVersion', c_wchar * 15),
        # session static info
        ('numberOfSessions', c_int32),
        ('numCars', c_int32),
        ('carModel', c_wchar * 33),
        ('track', c_wchar * 33),
        ('playerName', c_wchar * 33),
        ('playerSurname', c_wchar * 33),
        ('playerNick', c_wchar * 33),
        ('sectorCount', c_int32),
        # car static info
        ('maxTorque', c_float),
        ('maxPower', c_float),
        ('maxRpm', c_int32),
        ('maxFuel', c_float),
        ('suspensionMaxTravel', c_float * 4),
        ('tyreRadius', c_float * 4),
        ('maxTurboBoost', c_float),
        ('deprecated_1', c_float),
        ('deprecated_2', c_float),
        ('penaltiesEnabled', c_int32),
        ('aidFuelRate', c_float),
        ('aidTireRate', c_float),
        ('aidMechanicalDamage', c_float),
        ('aidAllowTyreBlankets', c_int32),
        ('aidStability', c_float),
        ('aidAutoClutch', c_int32),
        ('aidAutoBlip', c_int32),
        ('hasDRS', c_int32),
        ('hasERS', c_int32),
        ('hasKERS', c_int32),
        ('kersMaxJ', c_float),
        ('engineBrakeSettingsCount', c_int32),
        ('ersPowerControllerCount', c_int32),
        ('trackSPlineLength', c_float),
        ('trackConfiguration', c_wchar*33),
        ('ersMaxJ', c_float),
        ('isTimedRace', c_int32),
        ('hasExtraLap', c_int32),
        ('carSkin', c_wchar*33),
        ('reversedGridPositions', c_int32),
        ('PitWindowStart', c_int32),
        ('PitWindowEnd', c_int32)
    ]


class SimInfo:
    def __init__(self):
        self._acpmf_physics = mmap.mmap(0, ctypes.sizeof(SPageFilePhysics), "acpmf_physics")
        self._acpmf_graphics = mmap.mmap(0, ctypes.sizeof(SPageFileGraphic), "acpmf_graphics")
        self._acpmf_static = mmap.mmap(0, ctypes.sizeof(SPageFileStatic), "acpmf_static")
        self.physics = SPageFilePhysics.from_buffer(self._acpmf_physics)
        self.graphics = SPageFileGraphic.from_buffer(self._acpmf_graphics)
        self.static = SPageFileStatic.from_buffer(self._acpmf_static)

    def close(self):
        self._acpmf_physics.close()
        self._acpmf_graphics.close()
        self._acpmf_static.close()

    def __del__(self):
        self.close()

def read_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def initialize_dataframe(columns):
    return pd.DataFrame(columns=columns)

def append_to_dataframe(df, data):
    return df._append(data, ignore_index=True)

def save_dataframe_to_csv(df, filename):
    df.to_csv(f"data/logs/telemetry/{filename}", index=False)

def collect_telemetry(interval=0.2, session_duration=5):
    sim_info = SimInfo()
    start_time = time.time()  # Use time.time() for the start time
    filename = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Define the columns for your dataframe
    columns = ['timestamp', 'gas', 'brake', 'speedKmh', 'rpms', 'gear']  # Add more as needed
    df = initialize_dataframe(columns)

    while time.time() - start_time < session_duration:
        # Create a dictionary for the current set of telemetry data
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),  # Corrected datetime usage
            'gas': sim_info.physics.gas,
            'brake': sim_info.physics.brake,
            'speedKmh': sim_info.physics.speedKmh,
            'rpms': sim_info.physics.rpms,
            'gear': sim_info.physics.gear,
            # Add more data points as needed
        }
        print(data)
        df = append_to_dataframe(df, data)
        # Wait before the next read
        time.sleep(interval)  # This can indeed be adjusted as needed

    save_dataframe_to_csv(df, filename)
    sim_info.close()  # close the memory maps