from controller import Supervisor

from utils.component_manager import ComponentManager
from utils.position_related import TargetManager
from utils.random_policy import RandomPolicy, calculated_max_steps
from utils.homing import HomingBehaviour
from utils.logger import getEpisodeDataFrame, getSaveDirectory


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


# OBJECT INITIALIZATION
#########################

target_manager = TargetManager(gps, inertial_unit)
episode_df = getEpisodeDataFrame()
policy_manager = RandomPolicy(component_manager, target_manager, calculated_max_steps)
homing_behaviour = HomingBehaviour(robot, component_manager, target_manager, episode_df)

#########################


scene_id = 0
num_episodes = 50
seed = 42

episode_iterator = iter(range(num_episodes))
current_episode = next(episode_iterator)

is_revealed = False
is_reached = False


# CONTROL LOOP
while robot.step(timestep) != -1:
    
    # rl search phase    
    if not is_revealed:
        episode_dict = policy_manager.runEpisode(current_episode, seed, scene_id)
        
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
            print("Training Complete")
            
            save_dir = getSaveDirectory(policy='random')
            filename = f'{scene_id}-{num_episodes}-{seed}.csv'
            episode_df.to_csv(save_dir / filename)
            
            robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            break