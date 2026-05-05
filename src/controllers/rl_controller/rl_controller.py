import os
import torch
from controller import Supervisor

from utils.component_manager import ComponentManager
from utils.position_related import TargetManager
from utils.sensor_actuator.logger import getEpisodeDataFrame, getSaveDirectory, setAllSeeds

from utils.rl_specific.dqn_manager import DQnManager
from utils.dqn_policy import DQnPolicy, calculated_max_steps


robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# SENSOR / ACTUATOR INITIALIZATION
#########################

component_manager = ComponentManager(
    robot, timestep, 
    distance=True, 
    position=True, 
    gps=True, 
    inertial_unit=True, 
    motors=True
    ).enable()

gps = component_manager['gps']
inertial_unit = component_manager['inertial_unit']

#########################


# EXPERIMENT PARAMETERS
#########################

seed = int(os.getenv('SEED', 42))
num_episodes = int(os.getenv('NUM_EPISODES', 2000))
policy = os.getenv('POLICY', 'dqn')
scene_id = int(os.getenv('SCENE_ID', 0))
parent_scene = int(os.getenv('PARENT_SCENE', -1))
eval = os.getenv('EVAL', 'False')
eval = eval == 'True'

model_params_filename = os.getenv ('PARAMS_NAME', None)  
selective_replay_filename = os.getenv('SELECTIVE_REPLAY_NAME', None)
ewc_state_filename = os.getenv('EWC_STATE_NAME', None)

#########################


setAllSeeds(seed)

save_dir = getSaveDirectory(policy)

if model_params_filename is not None:
    model_params_path = save_dir / model_params_filename
else: 
    model_params_path = None

if selective_replay_filename is not None:
    selective_replay_buffer = torch.load(save_dir / selective_replay_filename, weights_only=False)
else: 
    selective_replay_buffer = {0: None, 1: None}
    
if ewc_state_filename is not None:
    ewc_state_path = save_dir / ewc_state_filename
else:
    ewc_state_path = None


# OBJECT INITIALIZATION
#########################

episode_df = getEpisodeDataFrame()
target_manager = TargetManager(gps, inertial_unit)

dqn_manager = DQnManager(
    policy=policy,
    scene_id=scene_id,
    model_params=model_params_path,
    selective_replay_buffer=selective_replay_buffer,
    ewc_state_path=ewc_state_path,
    eval=eval
    )

dqn_policy = DQnPolicy(
    policy=policy,
    scene_id=scene_id,
    robot=robot,
    dqn_manager=dqn_manager, 
    target_manager=target_manager, 
    component_manager=component_manager, 
    max_steps=calculated_max_steps,
    eval=eval
    )

#########################


episode_iterator = iter(range(num_episodes))
current_episode = next(episode_iterator)

episode_done = False


# CONTROL LOOP
while robot.step(timestep) != -1:
    
    if not episode_done:
        episode_done = dqn_policy.runEpisode(
            episode=current_episode,
            seed=seed,
            episode_df=episode_df
            )
        
    # upon episode completion    
    else:
        try:
            current_episode = next(episode_iterator)
            episode_done = False
            
        except StopIteration:
            print('Training Complete')
            
            train_eval = 'train' if not eval else 'eval'
            parent_label = '_' if parent_scene == -1 else parent_scene

            filename = f'logs-{train_eval}-{parent_label}-{scene_id}.csv'
                
            episode_df.to_csv(save_dir / filename)
            print('Training logs saved')
            
            if not eval:
                filename = f'model-{parent_label}-{scene_id}.pt'
                dqn_manager.saveModel(save_dir / filename)
                print('Model parameters saved')
            
            # save CRL info
            dqn_policy.saveSelectiveReplayBuffer(save_dir, selective_replay_buffer)
            dqn_policy.saveStateEWC(save_dir)
            
            # exit webots
            robot.simulationQuit(0)