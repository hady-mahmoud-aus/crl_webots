from pathlib import Path
import pandas as pd
import re
import json

def getAverageSearchEfficiency(df: pd.DataFrame):
    unique_cells_covered = df['unique_cells_covered']
    collisions = df['collisions']
    steps = df['decision_steps']
    
    df['search_efficiency'] = (unique_cells_covered - collisions) / steps
    
    return round(df['search_efficiency'].mean(), 3)

def getSuccessRate(df):
    return round(df['reached'].mean(), 3)

def findEvalFiles(directory: str | Path) -> list[Path]:
    """Return .csv files in a directory whose filenames contain 'eval'."""
    directory = Path(directory)
    pattern = re.compile(r".*eval.*\.csv$", re.IGNORECASE)

    return [
        path
        for path in directory.iterdir()
        if path.is_file() and pattern.search(path.name)
    ]

root = Path.cwd()

policy = input("Enter policy name (dqn, dqn_replay, dqn_ewc, dqn_replay_ewc): ")

runs_dir = root / 'runs' / policy

csv_files = findEvalFiles(runs_dir)

metrics = dict()

for file in csv_files:
    df = pd.read_csv(file)
    
    temp = dict()
    
    temp['success_rate'] = getSuccessRate(df)
    temp['average_search_efficiency'] = getAverageSearchEfficiency(df)
    
    metrics[file.name] = temp


filename = f'{policy}-metrics.json'
with open(runs_dir / filename, 'w') as output_file:
    json.dump(metrics, output_file, indent=4)
