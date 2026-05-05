from helper import runOneJob, TRAIN_EPISODES, EVAL_EPISODES, MODEL_NAMES


policy = "dqn_ewc"
MODEL_0, MODEL_01, MODEL_12, _, _ = MODEL_NAMES

EWC_0 = "ewc_state-0.pt"
EWC_01 = "ewc_state-0-1.pt"


SCHEDULE = [
    # Train T1 from scratch. Saves model-_-0.pt and ewc_state-0.pt.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Evaluate T1 after training T1.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": -1,
        "PARAMS_NAME": MODEL_0,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T2 from T1 model using T1 EWC state.
    # Saves model-0-1.pt and ewc_state-0-1.pt.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_0,
        "EWC_STATE_NAME": EWC_0,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Evaluate T2 after training T2.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_01,
        "EWC_STATE_NAME": EWC_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Evaluate old T1 after training T2.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 0,
        "PARAMS_NAME": MODEL_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Train T3 from T1->T2 model using accumulated T1+T2 EWC state.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_01,
        "EWC_STATE_NAME": EWC_01,
        "POLICY": policy,
        "NUM_EPISODES": TRAIN_EPISODES,
        "EVAL": "False",
    },

    # Evaluate T3 after training T3.
    {
        "SCENE_ID": 2,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
        "EWC_STATE_NAME": EWC_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Evaluate old T2 after training T3.
    {
        "SCENE_ID": 1,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
        "EWC_STATE_NAME": EWC_01,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },

    # Evaluate old T1 after training T3.
    {
        "SCENE_ID": 0,
        "PARENT_SCENE": 1,
        "PARAMS_NAME": MODEL_12,
        "POLICY": policy,
        "NUM_EPISODES": EVAL_EPISODES,
        "EVAL": "True",
    },
]


for job in SCHEDULE:
    runOneJob(job)

print("\nAll scheduled runs complete.")