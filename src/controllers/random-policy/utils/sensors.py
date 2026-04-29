from controller import Robot
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


def readSensors(sensors: dict, type = None):
    readings = {}
    for name, sensor in sensors.items():
        if type == "distance":
            min, max = 50, 1800
            reading = minMax(sensor.getValue(), min, max)
            
        else: reading = sensor.getValue()
        
        readings[name] = reading
    
    return readings

def minMax(x, min, max):
    return (x - min) / (max - min)


def readGPS(gps) -> dict:
    axes = ['x', 'y']
    reading = gps.getValues()[:2]
    
    return {axis: clean_zero(value) for axis, value in zip(axes, reading)}


def readHeading(inertial_unit) -> dict:
    theta =  inertial_unit.getRollPitchYaw()[2]
    
    return {"sin": clean_zero(sin(theta)), "cos": clean_zero(cos(theta))}

def clean_zero(value, eps=1e-9): # -0.0000 -> 0 | stabilizes readings at boundaries
    if abs(value) < eps:
        return 0.0
    return value