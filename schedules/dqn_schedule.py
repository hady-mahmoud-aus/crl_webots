from helper import runOneJob, TRAIN_EPISODES, EVAL_EPISODES, MODEL_NAMES


policy = "dqn"
MODEL_0, MODEL_01, MODEL_12, MODEL_1, MODEL_2 = MODEL_NAMES


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
        "PARAMS_NAME": MODEL_0,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T2 from T1 model.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_0,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T2 after training T2.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T1 after training T2.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T3 from T2 model.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_01,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Eval T3 after training T3.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T2 after training T3.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Eval old T1 after training T3.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
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
        "PARAMS_NAME": MODEL_1,
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
        "PARAMS_NAME": MODEL_2,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },
]


for job in SCHEDULE:
    runOneJob(job)

print("\nAll scheduled runs complete.")
