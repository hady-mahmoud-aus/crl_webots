from controller import Supervisor

from utils.component_manager import ComponentManager
from utils.position_related import TargetManager
from utils.homing import HomingBehaviour
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

scene_id = 0
num_episodes = 2
seed = 42
policy = 'dqn'

#########################

setAllSeeds(seed)

# OBJECT INITIALIZATION
#########################

target_manager = TargetManager(gps, inertial_unit)
episode_df = getEpisodeDataFrame()
homing_behaviour = HomingBehaviour(robot, component_manager, target_manager, episode_df)

dqn_manager = DQnManager()
dqn_policy = DQnPolicy(dqn_manager, component_manager, target_manager, calculated_max_steps)

#########################


episode_iterator = iter(range(num_episodes))
current_episode = next(episode_iterator)

is_revealed = False
is_reached = False


# CONTROL LOOP
while robot.step(timestep) != -1:
    
    # rl search phase    
    if not is_revealed:
        episode_dict = dqn_policy.runEpisode(current_episode, seed, scene_id)
        
        if episode_dict:
            if episode_dict['timeout_before_reveal']:
                episode_df.loc[len(episode_df)] = episode_dict # append to df inplace
                
                is_reached = True # skip homing
                
                homing_behaviour.resetProtocol()
        
        is_revealed = bool(episode_dict)
    
    # determinisically home to target
    elif not is_reached:
        is_reached = homing_behaviour.toTarget(episode_dict)
        
    # upon episode completion    
    elif is_reached:
        try:
            current_episode = next(episode_iterator)
            
            is_revealed = False
            is_reached = False
            
        except StopIteration:
            print('Training Complete')
            
            save_dir = getSaveDirectory(policy)
            
            logs_filename = f'data-{scene_id}-{num_episodes}-{seed}.csv'
            episode_df.to_csv(save_dir / logs_filename)
            
            model_filename = f'params-{scene_id}-{num_episodes}-{seed}.pt'
            dqn_manager.saveModel(save_dir / model_filename)
            
            print(f'Training logs and model parameters saved to {save_dir}')
            
            robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            break