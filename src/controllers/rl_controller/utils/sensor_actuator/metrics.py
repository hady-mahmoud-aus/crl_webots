
def getSearchEfficiency(unique_coverage, total_steps, n_collisions):
    return (unique_coverage - n_collisions) / total_steps