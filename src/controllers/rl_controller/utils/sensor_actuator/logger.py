import pandas as pd
from pathlib import Path
from typing import Literal
import random, torch, numpy


def getSaveDirectory(
    policy: Literal[
        'random', 
        'dqn', 
        'dqn_replay',
        'dqn_ewc',
        'dqn_replay_ewc'
        ]
    ):
    cwd = Path.cwd()
    project_root = next(
        p for p in (cwd, *cwd.parents)
        if p.name == "CRL"
        )
    
    path = project_root / 'runs' / policy
    path.mkdir(parents=True, exist_ok=True)
    
    return path

episode_dict = {
    'episode': pd.NA,
    'scene_id': pd.NA,
    'seed': pd.NA,

    'revealed': False,
    'reached': False,
    'timeout': False,

    'unique_cells_covered': pd.NA,
    'reward': pd.NA,
    'collisions': pd.NA,
    'decision_steps': pd.NA,
    }

def getEpisodeDataFrame():
    return pd.DataFrame(columns=episode_dict.keys())

def setAllSeeds(seed):
    random.seed(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)
