from pathlib import Path
import subprocess
import os
import platform
import time


REPO_NAME = "crl_webots"
WEBOTS_EXE = r"webots"

TRAIN_EPISODES = 2000
EVAL_EPISODES = 100

MODEL_NAMES = ("model-_-0.pt", "model-0-1.pt", "model-1-2.pt", "model-_-1.pt", "model-_-2.pt")



def getRootDirectory() -> Path:
    cwd = Path.cwd()
    project_root = next(
        p for p in (cwd, *cwd.parents)
        if p.name == REPO_NAME
    )
    return project_root

def getSaveDirectory(policy) -> Path:
    return getRootDirectory() / "runs" / policy


PROJECT_ROOT = getRootDirectory()

SCENE_TO_WORLD = {
    0: PROJECT_ROOT / "src" / "worlds" / "scene_1_empty.wbt",
    1: PROJECT_ROOT / "src" / "worlds" / "scene_2_obstacles.wbt",
    2: PROJECT_ROOT / "src" / "worlds" / "scene_3_dynamic.wbt",
}


def cleanupWebots():
    system = platform.system()

    if system == "Windows":
        commands = [
            ["taskkill", "/F", "/IM", "webots-bin.exe"],
            ["taskkill", "/F", "/IM", "webots.exe"],
        ]
    else:
        commands = [
            ["pkill", "-f", "webots-bin"],
            ["pkill", "-f", "webots"],
        ]

    for cmd in commands:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    time.sleep(3)


def runOneJob(job):
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
    print(f"Policy: {job.get('POLICY')}")
    print(f"Params: {job.get('PARAMS_NAME') or 'None'}")
    print(f"SSER memory: {job.get('SELECTIVE_REPLAY_NAME') or 'None'}")
    print(f"Eval: {job.get('EVAL')}")

    result = subprocess.run(cmd, env=env)

    cleanupWebots()

    if result.returncode != 0:
        raise RuntimeError(
            f"Webots run failed for scene {scene_id} with code {result.returncode}"
        )
