from math import pi
import pandas as pd
from copy import deepcopy
from controller import Supervisor

from .actions import turnByAngle, forwardByDistance, actionComplete
from .position_related import TargetManager
from .component_manager import ComponentManager
from .motors import setVelocityAll
from .position_related import resetPosition


restart_countdown = 1


class HomingBehaviour: 
    bearing_threshold = pi / 12
    
    def __init__(
        self, 
        robot: Supervisor,
        component_manager: ComponentManager, 
        target_manager: TargetManager, 
        episode_df: pd.DataFrame
        ):
        
        self.robot = robot
        self.target_manager = target_manager
        self.position_sensors = component_manager['position']
        self.motors = component_manager['motors']
        
        self.episode_df = episode_df
        
        self.current_target = None
        self.start_time = None
        
        
    def toTarget(self, episode_dict) -> bool:
        
        # start new episode {restart_countdown} seconds after finding target
        # generate new target
        if (self.start_time is not None): 
            if (self.robot.getTime() - self.start_time) >= restart_countdown:
                
                episode_dict['reached'] = True
                self.episode_df.loc[len(self.episode_df)] = episode_dict # append to df inplace
                
                self.start_time = None 
                
                self.resetProtocol()
                
                return True
            
            return False
        
        # no action taking place
        elif self.current_target is None:
            
            bearing = self.target_manager.getBearing()
            self.current_target = turnByAngle(bearing, self.motors, self.position_sensors, self.bearing_threshold)

            if self.current_target is None:
                
                distance = self.target_manager.getDistance()
                self.current_target = forwardByDistance(distance, self.motors, self.position_sensors)
        
        elif actionComplete(self.current_target, self.position_sensors):
            setVelocityAll(self.motors, 0.0)
            self.current_target = None 
            
            if self.target_manager.isReached():
                print(f"Target found") 
                self.start_time = self.robot.getTime()
                
        return False

    def resetProtocol(self):
        setVelocityAll(self.motors, 0.0)
        resetPosition(self.robot)
        self.target_manager.getNewTarget()