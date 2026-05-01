from controller import Robot

from typing import Literal
from math import sin, cos

front_sensor_names = ['ps0', 'ps7']
collision_value = 0.1 # [0, 1] Normalized

def getDistanceSensors(robot: Robot) -> dict:
    sensors =  {f"ps{i}": robot.getDevice(f"ps{i}")for i in range(8)}
    
    return sensors

def getPositionSensors(robot: Robot) -> dict:
    return {
        'right': robot.getDevice('right wheel sensor'),
        'left': robot.getDevice('left wheel sensor')
    }



def enableSensors(sensors: dict, sampling_period):
    for sensor in sensors.values():
        sensor.enable(sampling_period)



def readSensors(sensors: dict, type: Literal["distance"] = None, verbose=False):
    
    def minMax(x, min, max):
        return (x - min) / (max - min)
    
    readings = {} if verbose else []
    
    for name, sensor in sensors.items():
        if type == "distance":
            min, max = 50, 1800
            reading = minMax(sensor.getValue(), min, max)
            
        else: reading = sensor.getValue()
        
        if not verbose:
            readings.append(reading)
            
        else: readings[name] = reading
    
    return readings


def readGPS(gps, verbose=False):
    reading = gps.getValues()[:2]
    
    if not verbose: return reading
    
    axes = ['x', 'y']
    
    return {axis: clean_zero(value) for axis, value in zip(axes, reading)}


def readHeading(inertial_unit, verbose=False):
    theta =  inertial_unit.getRollPitchYaw()[2]
    
    sin_theta = clean_zero(sin(theta))
    cos_theta = clean_zero(cos(theta))
    
    if not verbose: return [sin_theta, cos_theta]
    
    return {"sin(theta)": sin_theta, "cos(theta)": cos_theta}

def clean_zero(value, eps=1e-9): # -0.0000 -> 0 | stabilizes readings at boundaries
    if abs(value) < eps:
        return 0.0
    return value