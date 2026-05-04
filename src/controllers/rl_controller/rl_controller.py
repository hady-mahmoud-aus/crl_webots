import os, torch
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
parent_scene = int(os.get_env('PARENT_SCENE', -1))
eval = os.getenv('EVAL', False)

model_params_path = os.getenv ('PARAMS_PATH', None)  

#########################


setAllSeeds(seed)

# OBJECT INITIALIZATION
#########################

episode_df = getEpisodeDataFrame()
target_manager = TargetManager(gps, inertial_unit)

dqn_manager = DQnManager(
    policy=policy,
    model_params=model_params_path, 
    eval=eval
    )

dqn_policy = DQnPolicy(
    policy=policy,
    robot=robot,
    dqn_manager=dqn_manager, 
    component_manager=component_manager, 
    target_manager=target_manager, 
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
            scene_id=scene_id,
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
            parent_label = '' if parent_scene == -1 else parent_scene
            
            save_dir = getSaveDirectory(policy)
            
            logs_filename = f'logs-{train_eval}-{parent_label}-{scene_id}.csv'
            episode_df.to_csv(save_dir / logs_filename)
            print(f'Training logs saved')
            
            if not eval:
                model_filename = f'model-{train_eval}-{parent_label}-{scene_id}.pt'
                dqn_manager.saveModel(save_dir / model_filename)
                print(f'Model parameters saved')
            
            # save CRL info
            
            
            
            
            # exit webots
            robot.simulationQuit(0)