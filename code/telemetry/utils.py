import mmap
import functools
import ctypes
import time
from datetime import datetime
import pandas as pd
from profiles import profiles
from constants import *
import json
import yaml
from ctypes import c_int32, c_float, c_wchar

def load_config(config_path="config.yaml"):
    """ Load the YAML configuration file. """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

class PhysicsInfo(ctypes.Structure):
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


class GraphicInfo(ctypes.Structure):
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


class StaticInfo(ctypes.Structure):
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
        self._acpmf_physics = mmap.mmap(0, ctypes.sizeof(PhysicsInfo), "acpmf_physics")
        self._acpmf_graphics = mmap.mmap(0, ctypes.sizeof(GraphicInfo), "acpmf_graphics")
        self._acpmf_static = mmap.mmap(0, ctypes.sizeof(StaticInfo), "acpmf_static")
        self.physics = PhysicsInfo.from_buffer(self._acpmf_physics)
        self.graphics = GraphicInfo.from_buffer(self._acpmf_graphics)
        self.static = StaticInfo.from_buffer(self._acpmf_static)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # Close all mmap files safely
        self._acpmf_physics.close()
        self._acpmf_graphics.close()
        self._acpmf_static.close()

def collect_telemetry(profile_name, interval=0.2, session_duration=100):
    # Load the configuration and get profiles
    config = load_config()
    profiles = config.get('profiles', {})

    sim_info = SimInfo()
    start_time = time.time()
    filename = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    columns = profiles.get(profile_name, [])
    
    if not columns:
        raise ValueError(f"No data columns defined for profile: {profile_name}")

    # Create a DataFrame with specified columns plus a timestamp
    df = pd.DataFrame(columns=['timestamp'] + columns)

    while time.time() - start_time < session_duration:
        data = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}
        
        # Collect data for each field specified in the profile
        for column in columns:
            if hasattr(sim_info.physics, column):
                data[column] = getattr(sim_info.physics, column)
            elif hasattr(sim_info.static, column):
                data[column] = getattr(sim_info.static, column)
            elif hasattr(sim_info.graphics, column):
                data[column] = getattr(sim_info.graphics, column)
            else:
                data[column] = None  # Default to None if not found

        print(data)
        df = df.append(data, ignore_index=True)  # Use 'append' instead of '_append'
        time.sleep(interval)

    df.to_csv(f"data/logs/telemetry/{filename}", index=False)
    sim_info.close()
