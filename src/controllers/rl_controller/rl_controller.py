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

scene_id = 1
num_episodes = 1000
seed = 42
policy = 'dqn'

#########################

setAllSeeds(seed)

# OBJECT INITIALIZATION
#########################

episode_df = getEpisodeDataFrame()
target_manager = TargetManager(gps, inertial_unit)

dqn_manager = DQnManager()
dqn_policy = DQnPolicy(
    robot=robot,
    dqn_manager=dqn_manager, 
    component_manager=component_manager, 
    target_manager=target_manager, 
    max_steps=calculated_max_steps
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
            
            save_dir = getSaveDirectory(policy)
            
            logs_filename = f'data-{scene_id}-{num_episodes}-{seed}.csv'
            episode_df.to_csv(save_dir / logs_filename)
            
            model_filename = f'params-{scene_id}-{num_episodes}-{seed}.pt'
            dqn_manager.saveModel(save_dir / model_filename)
            
            print(f'Training logs and model parameters saved to {save_dir}')
            
            robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            break