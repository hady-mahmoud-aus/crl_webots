from math import pi
from controller import Supervisor

from .actions import turnByAngle, forwardByDistance, actionComplete
from .position_related import TargetManager
from .component_manager import ComponentManager
from .motors import setVelocityAll
from .position_related import resetPosition

class HomingBehaviour: 
    bearing_threshold = pi / 12
    
    def __init__(self, component_manager: ComponentManager, target_manager: TargetManager):
        self.component_manager = component_manager
        self.target_manager = target_manager
        
        self.current_target = None
        self.start_time = None
        
        
    def toTarget(self, robot: Supervisor) -> bool:
        position_sensors = self.component_manager['position']
        motors = self.component_manager['motors']
        
        # respawn 5 seconds after finding target
        if (self.start_time is not None): 
            if (robot.getTime() - self.start_time) >= 5:
                setVelocityAll(motors, 0.0)
                resetPosition(robot)
                return True
            
            return False
        
        # no action taking place
        if self.current_target is None:
            
            bearing = self.target_manager.getBearing()
            self.current_target = turnByAngle(bearing, motors, position_sensors, self.bearing_threshold)

            if self.current_target is None:
                
                distance = self.target_manager.getDistance()
                self.current_target = forwardByDistance(distance, motors, position_sensors)
        
        elif actionComplete(self.current_target, position_sensors):
            setVelocityAll(motors, 0.0)
            self.current_target = None 
            
            if self.target_manager.isReached(): self.start_time = robot.getTime()
                
        return False