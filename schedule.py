import os
import subprocess
from pathlib import Path


# FOR MODIFICATION
#########################

policy = "dqn" # change this manually, or change it 

policy = os.getenv("POLICY", policy) 

#########################


# DO NOT MODIFY
#########################

WEBOTS_EXE = r"webots"

PROJECT_ROOT = Path().cwd()
RUNS_DIR = PROJECT_ROOT / policy 
FILENAME = f'{train_eval}-{parent_label}-{scene_id}-{num_episodes}-{seed}.pt'

FILE_PATH = 


SCENE_TO_WORLD = {
    0: PROJECT_ROOT / "src" / "worlds" / "scene_1_empty.wbt",
    1: PROJECT_ROOT / "src" / "worlds" / "scene_2_obstacles.wbt",
    2: PROJECT_ROOT / "src" / "worlds" / "scene_3_dynamic.wbt",
}

SCHEDULE = [
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "PARAMS_PATH": "",
        "POLICY": policy,
    },
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "PARAMS_PATH": "",
        "POLICY": policy,
    },
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "PARAMS_PATH": "",
        "POLICY": policy,
    },
]

def run_one(job):
    scene_id = int(job["SCENE_ID"])
    world_path = SCENE_TO_WORLD[scene_id]

    env = os.environ.copy()
    env.update({key: str(value) for key, value in job.items()})

    cmd = [
        WEBOTS_EXE,
        "--batch",
        "--mode=fast",
        "--no-rendering",
        "--stdout",
        "--stderr",
        str(world_path),
    ]

    print(f"\n=== Running scene {scene_id} ===")
    print(f"World: {world_path}")
    print(f"Params: {job.get('PARAMS_PATH') or 'None'}")

    result = subprocess.run(cmd, env=env)

    if result.returncode != 0:
        raise RuntimeError(f"Webots run failed for scene {scene_id} with code {result.returncode}")

for job in SCHEDULE:
    run_one(job)

print("\nAll scheduled runs complete.")

#########################
