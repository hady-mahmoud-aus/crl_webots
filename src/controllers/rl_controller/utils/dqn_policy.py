import random
from collections import deque, namedtuple
from copy import deepcopy
from typing import Literal

from .cell_tracker import CellTracker
from .component_manager import ComponentManager
from .position_related import TargetManager, arena_size
from .actions import action, actionComplete, onCollision, reverse, forward_step_length
from .sensor_actuator.motors import setVelocityAll
from .rl_helper import getObservation, getReward
from .sensor_actuator.logger import episode_dict

from .rl_specific.buffer import ReplayBuffer
from .rl_specific.dqn_manager import DQnManager


# assuming optimal row-sweeping search
cells_per_row = arena_size / forward_step_length
calculated_max_steps = int((cells_per_row ** 2) + (6 * cells_per_row))

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

class DQnPolicy:
    def __init__(
        self, 
        dqn_manager: DQnManager,
        component_manager: ComponentManager,  
        target_manager: TargetManager,  
        max_steps = float('inf')
        ):
        
        self.distance_sensors = component_manager['distance']
        self.position_sensors = component_manager['position']
        self.motors = component_manager['motors']
        self.inertial_unit = component_manager['inertial_unit']
        gps = component_manager['gps']
        
        self.dqn_manager = dqn_manager
        
        self.cell_tracker = CellTracker(gps, self.inertial_unit)
        self.target_manager = target_manager
        
        self.total_reward = 0
        self.steps = 0
        self.max_steps = max_steps
        self.collisions = 0
        self.is_collision = 0
        self.dwell_count = 0 # steps spent in the same cell
        
        self.current_target = None
        
        self.buffer = ReplayBuffer(capacity=10000, min_transitions=500)   
        
        # used for tracking current and previous state, such that transition contains (s_t, s_t+1)
        self.states = deque(maxlen=2)
        self.previous_cell_status = None
        self.action_code = None
        

    def runEpisode(self, episode, seed, 
        scene_id: Literal[0, 1, 2], verbose = False): 
        
        if self.steps == 0: # beginning of episode
            self.initEpisode(episode, seed, scene_id)
        
        if self.current_target is None: # if no action is taking place
            
            # check if cell is same, visited, or unvisited
            cell_status = self.cell_tracker.checkCell()
            
            if verbose:
                print(f'Current cell: {self.cell_tracker.current_cell}, {cell_status}')
                print(self.cell_tracker.getLocalVisitedFlags(verbose=True))
            
            state = getObservation(self.distance_sensors, self.inertial_unit, self.cell_tracker)
            self.states.append(state)
            
            # in case of collision, transition already added
            if len(self.states) > 1 and not self.is_collision: # second step onwards
                if self.addTransition(cell_status): # if terminal state
                    return self.endEpisode()
            else: self.is_collision = 0    
            
            if len(self.buffer) >= self.buffer.min_transitions: 
                self.dqn_manager.optimizeModel(self.buffer)
                self.dqn_manager.softUpdate()
                
            self.action_code = self.dqn_manager.getAction(state.unsqueeze(dim=0))
            self.current_target = action(self.action_code, self.motors, self.position_sensors)
            
            # for transition storage
            self.previous_cell_status = cell_status
            
            self.steps += 1
        
        # interrupts mid-action in case of collision
        elif (not self.is_collision) and\
            onCollision(self.motors, self.position_sensors, self.distance_sensors, react=False):
            setVelocityAll(self.motors, 0)
                
            self.is_collision = 1
            self.collisions += 1
            
            state = getObservation(self.distance_sensors, self.inertial_unit, self.cell_tracker)
            self.states.append(state)
            # add transition upon collision
            if self.addTransition(self.previous_cell_status): # if terminal state
                    return self.endEpisode()
            
            self.current_target = reverse(self.motors, self.position_sensors)
        
        # upon completion of action or post-collision behavior
        elif actionComplete(self.current_target, self.position_sensors):
            setVelocityAll(self.motors, 0.0)
            self.current_target = None 
            
        return None

    def initEpisode(self, episode, seed, scene_id):
        print(f'Starting episode: {episode}')
        print(f'Target: {self.target_manager}')
        
        # for different but deterministic seed on each episode
        random.seed(seed + episode) 
            
        self.episode_dict = deepcopy(episode_dict)
        self.episode_dict['episode'] = episode
        self.episode_dict['scene_id'] = scene_id
        self.episode_dict['seed'] = seed

    def addTransition(self, cell_status) -> bool:
        if not self.is_collision:
            if cell_status == self.cell_tracker.CELL_SAME: self.dwell_count += 1
            else: self.dwell_count = 0
                
        # calculate dwell if applicable
        if self.dwell_count > 2:
            dwell = self.dwell_count - 2
        else: dwell = 0
        
        # check if within target reveal radius
        revealed = self.target_manager.isRevealed()
        if revealed: 
            print('Target revealed')
            self.episode_dict['revealed'] = True
        
        # calculate reward        
        reward = getReward(cell_status, self.is_collision, dwell, int(revealed))
        self.total_reward += reward
        
        timeout = self.steps >= self.max_steps if not revealed else False
        if timeout: 
            print('Max steps reached - episode terminated')
            self.episode_dict['timeout_before_reveal'] = True
            
        
        next_state = self.states[1] if not (revealed or timeout) else None

        transition = Transition(
            self.states[0],
            self.action_code,
            next_state,
            reward
        )

        self.buffer.push(transition)
        
        return True if revealed or timeout else False
    
    def endEpisode(self) -> dict:
        self.episode_dict['unique_cells_covered'] = self.cell_tracker.getCoverage()
        self.episode_dict['reward'] = round(self.total_reward, 3)
        self.episode_dict['collisions'] = self.collisions
        self.episode_dict['decision_steps'] = self.steps
        
        # reset internal states for new episodes
        self.total_reward = 0
        self.collisions = 0
        self.is_collision = 0
        self.steps = 0
        self.dwell_count = 0
        self.previous_cell_status = None
        self.action_code = None
        self.current_target = None
        self.states.clear()
        self.cell_tracker.reset()
        # will set new target after homing phase
        
        # will add episode to log dataframe after homing phase 
        return deepcopy(self.episode_dict)