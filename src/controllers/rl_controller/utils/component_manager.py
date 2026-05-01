from controller import Supervisor
from .sensors import getDistanceSensors, getPositionSensors, enableSensors
from .motors import getMotors


class ComponentManager:
    
    def __init__(
        self, 
        robot: Supervisor, 
        timestep,
        distance: bool = False, 
        position: bool = False, 
        gps: bool = False,
        inertial_unit: bool = False,
        motors: bool = False
        ):
        
        self.robot = robot
        self.timestep = timestep
        
        self.components = {
            'distance': getDistanceSensors(self.robot) if distance else distance,
            'position': getPositionSensors(self.robot) if position else position,
            'gps': self.robot.getDevice('gps') if gps else gps,
            'inertial_unit': self.robot.getDevice('inertial unit') if inertial_unit else inertial_unit,
            'motors': getMotors(self.robot) if motors else motors
        }
    
    def enable(self):
        for key, value in self.components.items():
            if not value or key == 'motors': continue
            
            if key == 'distance' or key == 'position': 
                enableSensors(value, self.timestep)
                
            else: value.enable(self.timestep)
            
        return self
            
    def __getitem__(self, key):
        return self.components[key]