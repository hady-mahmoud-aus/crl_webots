from controller import Supervisor
from collections import deque, namedtuple
from copy import deepcopy
from typing import Literal

from .cell_tracker import CellTracker
from .component_manager import ComponentManager
from .position_related import TargetManager, arena_size, resetPosition
from .actions import action, actionComplete, onCollision, forward_step_length
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
        robot: Supervisor,
        dqn_manager: DQnManager,
        component_manager: ComponentManager,  
        target_manager: TargetManager,  
        max_steps = float('inf'),
        ):
        self.robot = robot
        
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
        self.action_code = None
        self.previous_distance = 0
        
        self.homing = False



    def runEpisode(
        self, 
        episode, 
        seed, 
        scene_id: Literal[0, 1, 2], 
        episode_df,
        verbose = False
        ): 
        
        if self.steps == 0: # beginning of episode
            self.initEpisode(episode, seed, scene_id)
        
        
        if self.current_target is None: # if no action is taking place
            
            # check if cell is same, visited, or unvisited
            cell_status = self.cell_tracker.checkCell()
            
            if verbose:
                print(f'Current cell: {self.cell_tracker.current_cell}, {cell_status}')
                print(self.cell_tracker.getLocalVisitedFlags(verbose=True))
                
            # dwell management: ignore dwell after collisions
            if not self.is_collision:
                # update dwell
                if cell_status == self.cell_tracker.CELL_SAME: self.dwell_count += 1
                else: self.dwell_count = 0 # moved to new cell
                
                obs_dwell = self.dwell_count
            
            else: obs_dwell = 0
            
            # small-loop handling
            loop_score = self.cell_tracker.getLoopScore()
            
            homing = self.target_manager.isRevealed() if not self.homing else self.homing
                
            state = getObservation(
                distance_sensors=self.distance_sensors, 
                inertial_unit=self.inertial_unit, 
                cell_tracker=self.cell_tracker, 
                target_manager=self.target_manager,
                dwell_count=obs_dwell, 
                loop_score=loop_score,
                homing=homing
                )
            
            self.states.append(state)
            
            # in case of collision, transition already added
            if len(self.states) > 1: # second step onwards
                if self.addTransition(cell_status): # if terminal state
                    return self.endEpisode(episode_df)
            
            if len(self.buffer) >= self.buffer.min_transitions: 
                self.dqn_manager.optimizeModel(self.buffer)
                self.dqn_manager.softUpdate()
                
            self.action_code = self.dqn_manager.getAction(state.unsqueeze(dim=0))
            self.current_target = action(self.action_code, self.motors, self.position_sensors)
            
            self.steps += 1
        
        
        # interrupts mid-forward action in case of collision;
        elif not self.is_collision and\
            self.action_code == 0 and\
            onCollision(self.motors, self.position_sensors, self.distance_sensors, react=False):
                
            setVelocityAll(self.motors, 0)
            
            # block cell if collided into after forward motion
            self.cell_tracker.blockForward()
                
            self.is_collision = 1
            self.collisions += 1
            
            self.current_target = None
        
        
        # upon completion of action
        elif actionComplete(self.current_target, self.position_sensors):
            setVelocityAll(self.motors, 0.0)
            self.current_target = None 
            
            
        return False



    def initEpisode(self, episode, seed, scene_id):
        print(f'Starting episode: {episode}')
        print(f'Target: {self.target_manager}')
            
        self.episode_dict = deepcopy(episode_dict)
        self.episode_dict['episode'] = episode
        self.episode_dict['scene_id'] = scene_id
        self.episode_dict['seed'] = seed



    def addTransition(self, cell_status) -> bool:
                
        # calculate dwell
        dwell = max(0, self.dwell_count - 2)
        
        # if all surrounding cells are visited, remove revisit penalty to prevent getting stuck
        flags = self.states[0][:4]
        escape_mode = all(int(f) == 1 for f in flags)
        
        loop_score = self.cell_tracker.getLoopScore()
        
        # calculate reward        
        reward, self.previous_distance = getReward(
            target_manager=self.target_manager, 
            cell_status=cell_status, 
            collision=self.is_collision, 
            dwell_steps=dwell, 
            loop_score=loop_score, 
            previous_distance=self.previous_distance, 
            escape_mode=escape_mode,
            homing=self.homing
            )
        
        self.total_reward += reward
        
        # reset collision state
        self.is_collision = 0
        
        # check if within target reveal radius
        if self.target_manager.isRevealed() and not self.homing: 
            print('Target revealed')
            self.episode_dict['revealed'] = True
            
            self.previous_distance = self.target_manager.getDistance()
            self.homing = True
        
        # check if within target reach radius
        reached = self.target_manager.isReached()
        if reached: 
            print('Target reached')
            self.episode_dict['reached'] = True
        
        # check if max steps taken
        timeout = self.steps >= self.max_steps if not reached else False
        if timeout: 
            print('Max steps reached - episode terminated')
            self.episode_dict['timeout_before_reveal'] = True
            
        
        next_state = self.states[1] if not (reached or timeout) else None

        transition = Transition(
            self.states[0],
            self.action_code,
            next_state,
            reward
        )

        self.buffer.push(transition)
        
        done = True if reached or timeout else False
        
        return done



    def endEpisode(self, episode_df) -> dict:
        self.episode_dict['unique_cells_covered'] = self.cell_tracker.getCoverage()
        self.episode_dict['reward'] = round(self.total_reward, 3)
        self.episode_dict['collisions'] = self.collisions
        self.episode_dict['decision_steps'] = self.steps
        
        # append to df inplace
        episode_df.loc[len(episode_df)] = self.episode_dict 
        
        
        setVelocityAll(self.motors, 0.0)
        resetPosition(self.robot)
        self.resetStates()
        
        # will add episode to log dataframe after homing phase 
        return True
    
    def resetStates(self): 
        # reset internal states for new episodes
        self.total_reward = 0
        self.collisions = 0
        self.is_collision = 0
        self.steps = 0
        self.dwell_count = 0
        self.action_code = None
        self.current_target = None
        self.states.clear()
        self.homing = False
        
        self.cell_tracker.reset()
        self.target_manager.getNewTarget()