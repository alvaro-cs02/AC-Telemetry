import mmap
import functools
import ctypes
import csv
import time
import threading
from datetime import datetime
from configparser import ConfigParser
from constants import *
from ctypes import c_int32, c_float, c_wchar

def load_config(config_path="code/telemetry/config.ini"):
    config = ConfigParser()
    config.read(config_path)
    return config

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
        del self.physics
        del self.graphics
        del self.static

        self._acpmf_physics.close()
        self._acpmf_graphics.close()
        self._acpmf_static.close()

def collect_data(sim_info, columns):
    data = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}
    for column in columns:
        attribute = getattr(sim_info.physics, column, None)
        if attribute is None:
            attribute = getattr(sim_info.static, column, None)
        if attribute is None:
            attribute = getattr(sim_info.graphics, column, None)
        data[column] = attribute
    return data

def collect_telemetry(profile_name, interval=0.2):
    config = load_config()
    try:
        profiles = dict(config.items(profile_name))
    except Exception as e:
        print(f"Error loading profile '{profile_name}': {e}")
        return
    
    sim_info = SimInfo()
    filename = f"data/logs/telemetry/telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    columns = [key for key, value in profiles.items() if value.lower() == 'true']

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['timestamp'] + columns)
        writer.writeheader()

        running = threading.Event()
        running.set()  

        while running.is_set():
            data = collect_data(sim_info, columns)
            writer.writerow(data)
            time.sleep(interval)
