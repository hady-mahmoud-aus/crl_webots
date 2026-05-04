import os
import subprocess
from pathlib import Path


def getRootDirectory():
    cwd = Path.cwd()
    project_root = next(
        p for p in (cwd, *cwd.parents)
        if p.name == "crl_webots"
    )
    return project_root


policy = "dqn"

WEBOTS_EXE = r"webots"

PROJECT_ROOT = getRootDirectory()
SAVE_DIR = PROJECT_ROOT / "runs" / policy

SCENE_TO_WORLD = {
    0: PROJECT_ROOT / "src" / "worlds" / "scene_1_empty.wbt",
    1: PROJECT_ROOT / "src" / "worlds" / "scene_2_obstacles.wbt",
    2: PROJECT_ROOT / "src" / "worlds" / "scene_3_dynamic.wbt",
}

TRAIN_EPISODES = 2000
EVAL_EPISODES = 100

SCHEDULE = [
    # Train T1 from scratch.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T1 after training T1.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "PARAMS_NAME": "model-_-0.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T2 from T1 model.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": "model-_-0.pt",
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T2 after training T2.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": "model-0-1.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T1 after training T2.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": "model-0-1.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T3 from T2 model.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": "model-0-1.pt",
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T3 after training T3.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": "model-1-2.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T2 after training T3.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": "model-1-2.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T1 after training T3.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": "model-1-2.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T2 from scratch.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": -1,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T2 after training T2.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": -1,
        "PARAMS_NAME": "model-_-1.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T3 from scratch.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": -1,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T3 after training T3.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": -1,
        "PARAMS_NAME": "model-_-2.pt",
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
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
    print(f"Params: {job.get('PARAMS_NAME') or 'None'}")

    result = subprocess.run(cmd, env=env)

    if result.returncode != 0:
        raise RuntimeError(f"Webots run failed for scene {scene_id} with code {result.returncode}")


for job in SCHEDULE:
    run_one(job)

print("\nAll scheduled runs complete.")
