from helper import runOneJob, TRAIN_EPISODES, EVAL_EPISODES, MODEL_NAMES


policy = "dqn"
MODEL_0, MODEL_01, MODEL_12, MODEL_1, MODEL_2 = MODEL_NAMES


SCHEDULE = [
    # Eval T3 after training T3.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": -1,
        "PARAMS_NAME": MODEL_2,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },
]


for job in SCHEDULE:
    runOneJob(job)

print("\nAll scheduled runs complete.")
