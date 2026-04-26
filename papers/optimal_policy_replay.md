# Optimal Policy Replay: A Simple Method to Reduce Catastrophic Forgetting in Target Incremental Visual Navigation

**Authors:** Xinting Li; Shizhou Zhang; Yue Lu; Kerry Dang; Lingyan Ran; Peng Wang  
**Published in:** 2023 China Automation Congress (CAC)  
**Conference dates:** 17–19 November 2023  
**Date added to IEEE Xplore:** 19 March 2024  
**DOI:** 10.1109/CAC59555.2023.10450433  
**Conference location:** Chongqing, China

> **Conversion notes:** Figures and repeated IEEE interface text were omitted. Equations were converted to LaTeX where readable. Table I’s body was not present in the provided pasted text; only its caption was present, so the table values are not included. See **Math readability notes** at the end for ambiguous equation fragments in the pasted source.

## Abstract

Visual navigation is a critical task in robotics and artificial intelligence. In recent years, reinforcement learning-based approaches have gained popularity for visual navigation. However, existing methods lack flexibility in learning multiple navigation targets and suffer from catastrophic forgetting. To address these challenges, we propose a novel paradigm called “target incremental visual navigation” and introduce a method called Optimal Policy Replay (OPR). Target incremental visual navigation aims to study the performance of visual navigation in continuous learning of navigation targets. OPR enables continuous learning of navigation targets without the need for relearning all targets. Our method divides the learning process into on-policy and off-policy stages and stores only the optimal experiences in memory. Experimental results show that OPR effectively alleviates catastrophic forgetting and achieves good performance with a small memory size.

## I. Introduction

Visual navigation is a fundamental problem in robotics and artificial intelligence. The target-driven visual navigation task involves commanding an agent to search for a given object in a 3D scene, using its egocentric camera to navigate around obstacles and determine the next step. In recent years, visual navigation has attracted increasing research interest in the fields of artificial intelligence and computer vision, with numerous potential applications such as automated home services, warehouse management, and the hotel industry.

Traditional approaches rely on map-based visual navigation methods. These methods explicitly decompose the navigation task into a set of sub-tasks, including mapping, localization, planning, and motion control [1]–[4], [21]. Due to the recent success of reinforcement-learning-based methods in robotic tasks [22]–[25], many mapless visual navigation works based on reinforcement learning have been proposed [7]–[12]. These methods typically take visual information and the navigation target as inputs and output the optimal actions the agent should take at each time step to achieve the specified target. Unlike traditional methods, reinforcement-learning-based approaches directly infer solutions from the current input, which is an end-to-end approach. As such, they require minimal manual engineering and serve as the foundation for new AI-driven visual navigation tasks.

However, current reinforcement-learning-based visual navigation methods typically employ training approaches that randomly select a navigation target at the beginning of each training task when learning multiple navigation targets. In this approach, the network model is capable of learning multiple navigation targets simultaneously. But when the agent is to expand the scope of navigation targets, existing methods must mix new and old goals and relearn. This process not only leads to significant resource wastage but also restricts the applicability of learning-based navigation algorithms. Hence, the model requires the capability of continuous learning of navigation targets. To investigate this matter, we propose a novel visual navigation paradigm known as “target incremental visual navigation.” In this paradigm, we enable the agent to learn navigation targets continuously in a predefined order, rather than randomly acquiring them.

To address the problem, we introduce a novel method called OPR (Optimal Policy Replay). OPR enables continuous learning of navigation targets without the need for relearning all targets, thereby mitigating resource wastage and expanding the potential applications of reinforcement-learning-based navigation algorithms. This method uses on-policy learning to learn the current navigation target, uses off-policy learning to learn only the learned navigation target, and stores only the optimal episode in memory to ensure the efficiency of off-policy learning. We found that the OPR method can effectively alleviate catastrophic forgetting in visual navigation.

In summary, our main contributions are as follows:

1. We introduce a novel paradigm called “target incremental visual navigation” to address the challenge of visual navigation.
2. We introduce a novel framework, OPR, for target incremental visual navigation. OPR divides the algorithm into on-policy learning and off-policy learning. Additionally, the memory stores only the optimal policy episode. OPR effectively alleviates catastrophic forgetting in visual navigation.
3. OPR also has strong performance with a small memory, indicating its broad applicability in various scenarios.

## II. Related Work

### A. Visual Navigation

Visual navigation is one of the fundamental problems for mobile robots. Traditional navigation methods typically use environmental maps for navigation and divide navigation tasks into three steps: mapping, localization, and path planning [1]–[6]. With the development of reinforcement learning, reinforcement learning has been applied to robot tasks, and navigation methods based on reinforcement learning are popular because they solve complex tasks through end-to-end methods.

Since Zhu et al. [7] proposed an end-to-end navigation model based on deep learning, which implicitly integrates localization, mapping, exploration, and semantic recognition, target-driven visual navigation has developed rapidly, and many efficient models have been proposed. Wortsman et al. proposed a meta-learning-based method [8] to dynamically adjust the navigation policy according to changes in the environment, and the agent learns self-supervised interaction losses to perform effective navigation. Lee et al. proposed object relation graphs to learn spatial relationships between the classes that appear in navigation to better guide agents in navigation [9]. They further proposed a novel Visual Transformer network (VTNet) to extract information feature representations in navigation [10]. This information feature representation not only encodes the relationship between objects, but also establishes a strong correlation with the navigation signal, which can better guide the agent’s next action.

In the task setting of multiple navigation goals, the above tasks randomly select navigation tasks before the start of each task, which can avoid catastrophic forgetting, but this method greatly limits the flexibility of the model. In actual situations, the model needs to have the ability of target incremental visual navigation.

### B. Continual Reinforcement Learning

The issue of catastrophic forgetting in neural networks has gained significant recognition: after training on the current task and directly training on the next task, the model exhibits high recognition accuracy on the new task but significant degradation in recognition accuracy on learned tasks. In recent years, people have renewed interest in overcoming catastrophic forgetting in reinforcement learning.

Kirkpatrick et al. proposed the Elastic Weight Consolidation (EWC) method [13], which restricts important weights from past tasks to change more slowly when learning new tasks. Rolnick et al. proposed the Continual Learning with Experience and Replay (CLEAR) method [14], which uses v-trace importance sampling to prevent catastrophic forgetting. Atkinson et al. proposed the Reinforcement Pseudo-Rehearsal (RePR) method [15], which generates pseudo-samples from a generative model to maintain knowledge about past tasks in the model. Kessler et al. proposed the UNcertainty guided Continual Learning (UNCLEAR) method [16], which preserves past knowledge by retaining the parameters of the output linear layer. Fernando et al. proposed the PathNet method [17], which uses genetic algorithms to find a path from the input to the output for each task in the neural network and separates the network parts used at the parameter level from new task training.

Most existing methods based on experience replay use FIFO or reservoir sampling to store experience. These methods cannot cope with the task of target incremental visual navigation very well because, due to limited memory size, they will forget past experience or affect the learning of new targets due to a large number of suboptimal experiences. Therefore, we only store the optimal experience in memory to ensure the efficiency of the model in off-policy learning.

## III. Method

### A. Problem Formulation

A navigation task consists of a scene $S$, an initial point $p$, and a target object $o$. The agent’s objective is to find the target object $o$ in the 3D environment from the initial position within a given number of steps. The agent’s action space is limited to six actions: `MoveAhead`, `RotateLeft`, `RotateRight`, `LookDown`, `LookUp`, and `Done`.

At each step, the agent receives an egocentric RGB image $s$ from the scene and a target object $o$, and the agent selects an action from the action space. A collection of all the steps from the beginning to the end of a task is called an episode. The agent successfully completes the navigation task if it performs the `Done` action when within 1 meter of an instance of the target object class and within the agent’s field of view.

Following the setting of target incremental visual navigation, we sequentially provide the target object to be learned. Once a target object has been learned, it will not be relearned when learning subsequent targets.

### B. Method Overview

OPR utilizes new experiences to learn the policy for the current target and replayed experiences to learn the policy for learned targets. Unlike typical algorithms based on experience replay, we only store the optimal experiences in memory to ensure that the agent can review the optimal policy for learned navigation targets when learning new ones.

We train a state feature extraction network and a value-policy network [9]. The input of the value-policy network is the output of the state feature extraction network, which is the high-level feature map of the current image. The outputs of the whole network are two functions: the policy function $\pi(a \mid s)$ and the Q-function $Q(s \mid a)$. The entire training process is divided into two stages: the on-policy stage and the off-policy stage.

In the on-policy stage, the agent learns the policy for the new target through interaction with the environment. In the off-policy stage, the agent reviews the learned policy using the optimal experiences of learned navigation targets stored in memory to prevent catastrophic forgetting.

### C. On-Policy Learning

In this stage, our objective is to train the agent to learn the optimal policy for the current target. When learning a new navigation target policy, the agent directly interacts with the environment. Training proceeds as in [19] by the A3C algorithm, and the policy gradient is given by:

$$
G_{\mathrm{on\text{-}policy}}
=
\sum_{t=1}^{T_n}
\left(
Q^{\pi_\theta}(s_t,a_t) - V^{\pi_\theta}(s_t)
\right)
\nabla \log \pi_\theta(a_t \mid s_t)
\tag{1}
$$

where $\theta$ denotes the parameters of the neural network, $\gamma \in [0,1)$ is the discount factor, $\pi_\theta(a_t \mid s_t)$ is the current policy, $Q^{\pi_\theta}(a_t \mid s_t)$ is an estimate of the action-value function, and

$$
V^{\pi_\theta}(s_t)
=
\sum_{i=0}^{k}
\pi_\theta(a_t \mid s_t)Q^{\pi_\theta}(a_t \mid s_t),
$$

where $k$ is the number of actions.

The pseudocode of the on-policy flow is shown in Algorithm 1. The agent chooses an initial state and a navigation target at the beginning of each task, subsequently interacts with the environment during task execution until the agent selects the action `Done` or reaches the maximum step, and updates the network based on the episode once the task concludes.

#### Algorithm 1: OPR On-Policy

```text
Reset gradients: dθ ← 0
Initialize parameters: θ′ ← θ
Get initial state x₀ and navigation target o

while Done is not selected and the maximum step is not exceeded do
    Get action: a_t = π(s_t | θ′)
    Get reward: r_t = R(· | s_t, a_t)
    Get Q function: Q(s_t, a_t)
    Get next state: s_{i+1} = f(· | a_t)
end while

Update network parameter: θ ← θ + αG_on-policy
```

### D. Off-Policy Learning

In the off-policy stage, unlike the common off-policy algorithm, we do not collect episodes during on-policy learning. Instead, we collect episodes after training when a navigation target reaches its maximum. In this way, the collected experience is the optimal experience for the current navigation target—assuming that the success rate of the task increases with the number of training times—which can minimize forgetting.

The episode stored in memory is

$$
\mathrm{episode}
=
\{(s_t,a_t,r_t,\pi_t,Q_t) \mid 1 \le t \le T\},
$$

and the target set is

$$
\mathrm{target}
=
(\mathrm{target}_1,\mathrm{target}_2,\ldots,\mathrm{target}_n),
$$

where $T$ is the total number of steps in an episode and $m$ is the memory size. The expression of memory is as follows:

$$
\mathrm{Memory}
=
\sum_{i=1}^{n}\frac{m}{n}\sum_{j=1}^{T}
(s_t,a_t,r_t,\pi_t,Q_t)
\tag{2}
$$

From a policy perspective, what is stored in memory is:

$$
\mathrm{Memory}
=
(\pi_1,\pi_2,\pi_3,\ldots,\pi_n)
\tag{3}
$$

The off-policy stage occurs several times after the on-policy stage has ended. Training proceeds as in [20] by the ACER off-policy learning algorithm, which uses Retrace $Q^{\mathrm{ret}}(a_t \mid s_t)$ to estimate $Q^\pi(a_t \mid s_t)$ and importance-weight truncation with bias correction to reduce variance for off-policy distribution shifts. While the ACER off-policy algorithm was designed to reduce variance and improve training stability, we find it also successfully corrects the distribution shift corresponding to the replay episode.

Formally, the policy gradient of the ACER off-policy algorithm is given by:

$$
\begin{aligned}
G_{\mathrm{off\text{-}policy}}
={}&
\bar{\rho}_t
\nabla_\theta \log \pi_\theta(a_t \mid x_t)
\left[
Q^{\mathrm{ret}}(x_t,a_t) - V_\theta(x_t)
\right] \\
&+
\mathbb{E}_{a \sim \pi}
\left(
\left[\frac{\rho_t(a)-c}{\rho_t(a)}\right]_+
\nabla_\theta \log \pi_\theta(a \mid x_t)
\left[
Q_\theta(x_t,a)-V_\theta(x_t)
\right]
\right).
\end{aligned}
\tag{4}
$$

where $\bar{\rho}_t$ is the truncated importance weight,

$$
\bar{\rho}_t = \min(c,\rho_t),
$$

with

$$
\rho_t = \frac{\pi_\theta(a_t \mid x_t)}{\mu(a_t \mid x_t)},
$$

and $[x]_+ = x$ if $x > 0$ and zero otherwise, with $c$ constant.

On the basis of ACER, we have added two losses [14], namely $L_{\mathrm{policy\text{-}loss}}$ and $L_{\mathrm{value\text{-}loss}}$. These two losses use KL divergence and the L2 norm, respectively, to fit the differences between the target policy and the behavioral policy. The pseudocode of the off-policy flow is shown in Algorithm 2. The agent selects an episode from memory and uses this episode to update network parameters through ACER’s off-policy algorithm.

#### Algorithm 2: OPR Off-Policy

```text
Reset gradients: dθ ← 0
Initialize parameters: θ′ ← θ
Get an episode from memory: {(s_t, a_t, r_t, π_t, Q_t) | t ∈ (1, …, k)}

for i ∈ (1, …, k) do
    Calculate Retrace: Q_ret(s_t, a_t) ← r_t + γQ_ret
    Update network parameter: θ ← θ + αG_off-policy
end for
```

### E. Overall Process

In this approach, a set of targets is first defined, and each target is iterated over. During each target iteration, policy updates are performed by invoking on-policy learning (Algorithm 1). In the process of policy updating, according to the predefined playback ratio $r$, a random number $k$ is generated using the Poisson distribution, which is used to determine the number of iterations of the off-policy learning algorithm (Algorithm 2). Through multiple off-policy optimizations, past experience can be more effectively utilized.

Next, at the end of each target iteration, we collect a certain amount of replay episodes and store them in memory. Specifically, by performing a certain number of environment interactions, we collect the state $s_t$, action $a_t$, reward $r_t$, policy $\pi_t$, and Q-value estimate $Q_t$ for each round. The memory capacity of each target is $m/n$ episodes. After collecting the optimal trajectory, the agent continues to learn the next navigation target.

Through this algorithm, we can learn the learned policy while learning the new target policy. This approach takes full advantage of both online and offline policy optimization to improve the efficiency and performance of the algorithms. The pseudocode of the complete algorithm flow is shown in Algorithm 3.

#### Algorithm 3: OPR

```text
Assume replay ratio r
Define target ∈ (1, …, n)

for i ∈ (1, …, n) do
    while the maximum number of episodes is not reached do
        Call OPR on-policy, Algorithm 1
        k ← Poisson(r)

        for j ∈ (1, …, k) do
            Call OPR off-policy, Algorithm 2
        end for
    end while

    for j ∈ (1, …, m/n) do
        Collect episodes (s_t, a_t, r_t, π_t, Q_t) and store them in memory
    end for
end for
```

## IV. Experiments

In our study, we trained and evaluated our approach in the AI2-THOR environment [7], which consists of 10 navigation targets:

```text
['AlarmClock', 'Book', 'Bowl', 'CoffeeMachine', 'Kettle',
 'Plate', 'Pan', 'Toaster', 'Pot', 'Fridge']
```

We used the reward function proposed in [8], where finding an object rewards the agent with 5, and taking a step results in a reward of -0.01. Our experiments focus on the plasticity and stability of the network to new navigation targets, so our experiments are carried out in the same environment in order to avoid the interference of different environments on the navigation model.

### A. Baseline

We present the experimental results of an actor-critic network trained without using experience replay. The curve of the network is presented in Figure 1, which shows the performance of the network on all tasks. Each color represents the performance on a different task, and the background color indicates the task on which the network is currently being trained. We saved 10 models for each navigation target and tested them on all previously learned navigation targets. Our results show that when experience replay is not used, the model forgets the previously learned tasks.

### B. OPR

Figure 2 displays the experimental results of using OPR to address catastrophic forgetting in visual navigation. The figure shows that the model trained with OPR performs significantly better than the model trained without OPR. One reason for this is that OPR uses experience replay, allowing the model to learn previously learned navigation targets while learning new ones. Additionally, OPR only saves the optimal policy in memory, avoiding the issue of forgetting caused by the standard FIFO policy or the existence of many suboptimal trajectories in memory as proposed in [18] using the Global Distribution Matching method.

### C. Limited-Size Memory

In reality, the storage space of memory is limited, and it is impossible to store infinitely. We trained a total of 10,000,000 episodes and set up four different sizes of memory to observe the performance changes: 50k, 30k, 5k, and 2k. In terms of performance, we observe that the network exhibits very good performance when the memory size is 50k and 30k.

**Table I. Quantitative results.** The authors use the average success rate to quantitatively evaluate the performance of each method based on all the above results.

> **Note:** The pasted source text did not include the numeric contents of Table I, only the caption above.

This suggests that a larger memory capacity helps the network better capture and utilize past experience. In contrast, we observe relatively poor performance of the network when the memory size is 2k. This suggests that a small memory capacity limits the network’s effective use of past experience, leading to a decrease in its performance in learning tasks. Unlike the method in [14], where half of the experience is stored in memory, the number of trajectories stored in our memory is only a small fraction of the total number of trajectories. Our approach effectively prevents forgetting and preserves the ability to solve past tasks even with a smaller memory module.

### D. Quantitative Analysis

In order to compare the performance of quantitative analytical methods and effectively capture the overall performance during continual learning, including the impact of catastrophic forgetting, we propose an evaluation metric called AS (average success):

$$
AS = \frac{1}{n}\sum_{i=1}^{n} S_i,
$$

where $n$ is the number of currently learned navigation targets, and $S_i$ is the success rate of the $i$-th navigation target. The values in the figure represent the test results of the agent on all learned targets after learning the current navigation target. Based on the results, while the average success rate of OPR decreases as the navigation target increases, it still exhibits a favorable balance between plasticity and stability when compared to other methods.

### E. Comparison to EWC and GDM

We compared our method with EWC [13] and GDM (Global Distribution Matching) [18]. We implemented and tested their approaches on our task. Firstly, GDM is also a replay-based method that uniformly stores experiences in memory during training. This leads to a large number of suboptimal trajectory samples being stored in memory, significantly affecting the model’s plasticity. Additionally, as new navigation targets are added to the memory, the proportion of excellent trajectories in the already poor-quality memory decreases, resulting in reduced model stability.

On the other hand, EWC employs regularization to penalize modifications to the gradients of previously learned navigation targets. Since EWC is entirely on-policy learning, it exhibits greater plasticity compared to GDM. However, similar to GDM, EWC also suffers from a phenomenon where failure to learn one target leads to poor learning of the remaining targets. As both EWC and GDM utilize previously learned knowledge, incorrect knowledge accumulates and negatively impacts subsequent learning.

## V. Conclusion

In this paper, we address the challenge of target-driven visual navigation by introducing a new paradigm called target incremental visual navigation. We propose a framework called OPR (Optimal Policy Replay) to enable continuous learning of navigation targets without relearning all targets. OPR utilizes on-policy learning to learn the current navigation target and off-policy learning to store the optimal policy for previously learned targets in memory. Our experiments show that OPR effectively mitigates catastrophic forgetting in visual navigation.
