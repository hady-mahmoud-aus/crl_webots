# Knowledge-Guided Continual Reinforcement Learning for Navigation

**Authors:** Peng Qin; Jianjian Zhao; Zhen Mei; Hainan Yang; Tao Zhao

## Abstract

Autonomous navigation is a core function of Internet of Things (IoT)-enabled robotic systems, particularly in applications such as smart warehousing, intelligent inspection, and collaborative logistics. Reinforcement learning (RL) has achieved remarkable progress in robotic navigation, but conventional RL methods typically rely on fixed task distributions, making it difficult to adapt to incremental multiscene navigation strategies that are common in dynamic IoT environments. Learning navigation across multiple scenes faces major challenges: catastrophic forgetting in sequential learning, where new scene learning overwrites prior knowledge, and sample inefficiency due to random exploration in complex environments. To address these challenges, this article proposes a knowledge-guided continual RL (KGCRL) approach. Built upon the deep deterministic policy gradient (DDPG) framework, KGCRL integrates elastic weight consolidation (EWC) to mitigate catastrophic forgetting by preserving critical parameters from previously learned tasks. Furthermore, a knowledge-guided learning mechanism is introduced to incorporate external knowledge, thereby improving exploration efficiency and stability. Experimental results in incremental scene navigation demonstrate that KGCRL significantly improves scene adaptability while reducing cross-scene performance degradation. These results validate the effectiveness and practicality of KGCRL, providing new insights for robot incremental scene navigation.

## Publication Details

- **Published in:** IEEE Internet of Things Journal, Volume 13, Issue 5, 01 March 2026
- **Pages:** 9535–9547
- **Date of Publication:** 17 December 2025
- **DOI:** 10.1109/JIOT.2025.3645269

## Nomenclature

| Symbol | Description |
|---|---|
| $T_k$ | Task k . |
| $\theta_{T_k}$ | Parameters of task-k policy. |
| $s/s'/a$ | State/next state action. |
| $D/D_{T_k}$ | Full/task-k dataset. |
| $F$ | Fisher matrix. |
| $C_{\{gd/g/c/e/s\}}$ | Reward parameters. |
| $M_{T_k}$ | Model after task k . |
| $F(T_k)$ | Forgetting after task k . |
| $FT(T_k)$ | Forward transfer after task k . |
| $\mu(s\mid\theta)$ | Policy. |
| $Q_\omega(s,a)$ | Critic network. |
| $a_G(\cdot)/\theta_G$ | Fusion function parameters. |
| $a_{ks}$ | Knowledge-system action. |
| $L_G^{T_k}$ | Fusion loss. |
| $L_Q^{T_k}$ | Critic loss. |
| $L_\mu^{T_k}$ | Policy loss. |
| ASR | Average success rate. |
| SASR | Scene average success rate. |

## I. Introduction

With the rapid development of the Internet of Things (IoT) and robotics, mobile robots have become key enablers in applications such as automated warehousing, intelligent logistics, environmental monitoring, and rescue operations. A typical navigation system integrates multiple functional modules-including perception, planning, and control-that collaboratively ensure the robot can reach a target location safely and efficiently [1]. Traditional map-based navigation methods, after years of development, are known for their robustness, interpretability, and engineering feasibility, and thus remain widely used. However, they often rely on sampling and optimization-based techniques as well as high-precision maps, while their dependence on multimodule coordination increases system complexity and reduces adaptability in dynamic environments.

Recently, with the advancement of deep learning, learning-based end-to-end navigation has gained attention by directly deriving control strategies from perceptual data, reducing reliance on explicit modeling and complex modular design [2]. However, reinforcement learning (RL)-based navigation methods still face two major challenges. First, the compatibility of RL algorithms with continual learning is limited. RL methods typically rely on a fixed task distribution [3], and when a new task arises, it is often treated as an independent learning process. In navigation applications, this manifests as separate navigation models for different scenes, requiring retraining when a new scene emerges, which results in low learning efficiency and poor adaptability. Second, traditional RL algorithms lack the utilization of prior knowledge [4]. Random exploration in complex environments may fail to collect useful data, causing convergence difficulties.

To address the aforementioned issues, the motivation of this study is to propose a knowledge-guided continual RL (KGCRL) method that not only incorporates the characteristics of continual learning but also fully utilizes prior knowledge. This approach aims to improve the learning ability, efficiency, and convergence of existing RL-based navigation methods in incremental scenes. Specifically, to mitigate catastrophic forgetting in sequential scene learning, elastic weight consolidation (EWC) is employed to identify and preserve parameters that are critical to previously learned scenes; to overcome sample inefficiency and instability caused by random exploration, a knowledge-guided exploration (KGE) mechanism is introduced to provide informative reference actions, improving data efficiency and convergence. These designs collectively improve the adaptability, learning efficiency of RL-based navigation across incremental scenes.

Based on this, this article proposes the KGCRL method, and the main work and contributions made are as follows.

This article extends the traditional RL navigation framework by incorporating the concept of continual learning. Instead of retraining per scene or jointly training across all scenes, KGCRL sequentially trains a single policy over incremental scene sequences. To preserve previously acquired knowledge, Fisher information is used to evaluate the importance of past policy parameters.

To alleviate the issues of previous strategy solidification hindering new scenario learning, a knowledge-guided learning strategy is proposed. This strategy integrates knowledge into exploration, additional rewards (ARs), and loss function construction, thereby improving the learning process from multiple perspectives.

Extensive validation of the proposed method was conducted through simulations and experiments, analyzing various features such as continual learning, prevention of forgetting, and performance improvement. Compared with existing methods, it demonstrates superior performance.

## II. Related Work

### A. RL for Robot Navigation

In the field of RL robot navigation, several improved methods have been proposed from several perspectives in recent years. In feature extraction, a novel extractor has been introduced to better capture spatiotemporal features for navigation, with validated generalization across environments [5]. In addition, a radar preprocessing method adjusting the far-near point ratio based on soft actor critic improves disparity in point cloud data, enhancing navigation [6]. For navigation architecture, an RL method utilizing virtual intermediate goals enables mapless navigation [7]. A hierarchical RL (HRL) approach improves learning efficiency by switching low-level controllers instead of directly outputting goals [8]. Another HRL method constructs a predictive spatial scoring model based on deep deterministic policy gradient (DDPG) to solve long-term decision-making problems [9]. Regarding rewards and constraints, a set of reward functions was designed in reward shaping of the DDPG to alleviate reward sparsity [10]. A curiosity-based exploration method was proposed with ARs [11]. A modular RL method with adaptive mixed-weight schemes enhances maze navigation [12], while another approach, based on proximal policy optimization, combines velocity and trajectory constraints with curriculum learning for smooth obstacle avoidance [13]. Although these studies have achieved promising results by optimizing different RL methods from various perspectives, they fail to address the continual learning challenges in novel scenes. Specifically, continual learning is inherently a sequential process, whereas existing methods either adapt to fixed task distributions or focus on joint training, thus being unsuitable for sequential learning across multiple scenes. In contrast, we formulate multiscene navigation learning as a continual learning process, where the parameter updates between old and new scenes are constrained to enhance continual learning capability.

### B. Continual Learning

Continual learning aims to learn to complete new tasks while retaining the ability to perform previously learned tasks, representing a long-standing challenge in the field of artificial intelligence. Existing methods fall into three main categories: data replay, regularization, and network expansion [14]. Data replay methods primarily involve storing data from previous tasks and reusing it when learning new tasks. Experience replay is employed to provide supervision to different layers of the model during training [15]. A context-aware memory recall strategy has been proposed for adaptive experience replay, which adjusts the replayed data based on context [16]. Unlike traditional data replay, generative models are used to synthesize new data, which serves as effective counterexamples to facilitate the learning of new classes [17]. Regularization-based methods prevent forgetting without storing data [18], such as learning without forgetting (LwF), which uses previous model outputs as soft labels [19]. Network expansion dynamically extends architectures as new tasks emerge [20]. Some methods adaptively adjust structures [21], while others increase depth for better representation and reduced memory load [22]. Despite advancements, most continual learning research focuses on image classification, with limited work on mobile robot navigation. Navigation tasks face constraints like inaccessible past data, limiting experience replay, while network expansion increases computational cost. To address these, our approach enhances RL continual learning through regularization techniques.

### C. Guided RL

Knowledge-guided RL enhances learning efficiency by leveraging external knowledge, with existing methods based on demonstrations, rules, knowledge graphs, prior policy, and reward shaping [4], [23], [24], [25], [26], [27], [28], [29]. Demonstration-based methods train expert models using human data to guide RL policies. For example, imitation constraints help soft actor-critic (SAC) models mimic expert behavior [4], while adaptive priority experience replay prevents excessive reliance on demonstrations [24]. Recent human-in-the-loop approaches further combine transfer learning with real-time human feedback to improve adaptation and safety in robot navigation [30]. Rule-based approaches use human-defined rules to guide exploration. Fuzzy rule systems improve learning efficiency [25], while a hybrid knowledge representation enhances the DDPG framework for navigation tasks [26]. In addition, common-sense knowledge can be explicitly embedded into the network topology to provide structured priors for learning [31]. Knowledge graphs aid decision-making by encoding relationships between entities. In recommendation tasks, they augment input states to improve efficiency [27]. Reward shaping integrates prior knowledge into rewards. A potential-based reward design helps optimize learning trajectories [29]. This research involves sequential learning in multiple scenes, and new scene learning is easily affected by the solidification of previous strategies. Therefore, we propose an external knowledge strategy to guide continual RL, focusing on improving learning efficiency and convergence in new scenes.

## III. Methodology

### A. Overview

Most current RL methods perform well on fixed task distributions, but their performance in incremental or sequential scenes remains limited. Specifically, learning subsequent tasks can modify previously learned parameters, leading to forgetting. Consolidating important parameters is a key approach to preserving knowledge, and based on this idea, EWC is employed to estimate parameter importance and enforce consolidation. In addition, random exploration in complex environments often fails to acquire useful information efficiently and may even prevent convergence. Leveraging useful external reference signals can reduce such blind exploration, and thus, we introduce a knowledge-guided module to improve single-task learning efficiency and mitigate negative transfer. Overall, the framework is illustrated in Fig. 1, and the notation summary in Nomenclature. In the data acquisition phase, where the agent interacts with the environment to gather information (such as radar point clouds and target data), in addition to the RL action, the action generated by the external knowledge policy (denoted by the dashed line) is used to guide the agent’s exploration. During the parameter update phase, both the EWC constraint (represented by the thick arrow) and the knowledge policy jointly guide the update of the parameters. After the scene transition, the optimal parameters learned from the previous scene are transferred to the subsequent scene. The specific implementation details are provided in Section IV. The proposed method exhibits the following characteristics.

**Remark 1 (Feature 1—Scene-Independent Continual Learning Capability).** Traditional end-to-end navigation strategy learning methods are difficult to learn multiple scenes in a sequential manner. The proposed method introduces EWC to protect key parameters from the influence of previous scenes and prevent catastrophic forgetting. In addition, when a new scene starts, there is no need to revisit data or environment from previous scenes, thus achieving scene-independent continual learning.

**Remark 2 (Feature 2—Multidimensional Utilization of Knowledge Strategies).** In traditional RL, exploration strategies often rely on random noise processes and are only guided by the critic for strategy updates, which may result in low exploration efficiency and difficulty in convergence. This article proposes a multidimensional knowledge utilization method that integrates exploration strategies, AR mechanisms, and objective functions to optimize the learning process of agents, especially in complex scenes that are difficult to handle through random exploration, thereby improving convergence and performance. In addition, in the continual learning setting, the solidification of previous strategies may hinder the learning of new scenes, and introducing knowledge guidance can alleviate the impact of strategy solidification.

### B. Problem Formulation

In multiscene robotic navigation, each scene is characterized by distinct obstacle layouts, obstacle types, and goal configurations, which in turn lead to different state-transition dynamics and reward structures. This setting closely aligns with the domain-incremental learning paradigm, where the state and action spaces remain fixed, but the underlying data distributions vary across scenes. Formally, we define a scene sequence Tk∈T={T1,T2,…,Tk,…} , where all scenes share the same state space S and action space A , but differ in their environment dynamics and reward functions due to scene variations. For each scene Tk , the agent seeks to learn a navigation policy πθ:S→A , parameterized by θ∈Rd , that maximizes the expected cumulative return

$$
\theta_{T_k}^{*}=\arg\max_{\theta\in\mathbb{R}^{d}} J_{T_k}(\theta)
\tag{1}
$$

where JTk(θ) denotes the expected return in scene Tk , considering factors such as goal-reaching, obstacle avoidance.

In the continual learning setting, when a new scene Tk+1 arrives, the following constraints are imposed to reflect practical requirements in robotic navigation.

The agent cannot access any data or environment interactions from previous scenes {T1,…,Tk} , as storing and revisiting all past environments is often infeasible in long-term deployments.

The network structure must remain fixed-no additional parameters or architecture expansion is allowed, to ensure bounded model size and computational cost under resource-constrained robotic platforms.

Experience replay and joint training are prohibited due to the absence of past scenes data, emphasizing the need for forward-transfer and knowledge retention without explicit storage.

Thus, the learning objective is to find parameters θ∗Tk+1 that adapt to the new scene Tk+1 , while retaining performance on previous scene Tk

$$
\theta_{T_{k+1}}^{*}=\arg\max_{\theta\in\mathbb{R}^{d}}
\left[\hat{J}_{T_k}(\theta)+J_{T_{k+1}}(\theta)\right]
\tag{2}
$$

where J^Tk(θ) is an estimated surrogate objective that approximates performance on scene Tk without using its data or environment. This formulation ensures the agent can continually learn navigation skills in new environments while preserving prior knowledge, without relying on experience replay or network expansion, and is particularly suited for real-world robotics applications with storage and interaction constraints.

**Remark 3.** This problem setting highlights the practical gap between multiscene navigation and traditional methods. Classic planning algorithms such as A∗ and RRT can generate efficient trajectories in a single scene, but lack knowledge transfer across different environments. Similarly, standard RL training can achieve multiscene navigation through cross-training, but it cannot adapt to scenes with significant differences and requires training from scratch. In contrast, continual RL enables agents to gradually acquire navigation skills in new environments while retaining their previous abilities, making them particularly suitable for long-term robot deployment.

### C. Markov Decision Process

#### 1. State Space

The state space S consists of the environmental information, the target information, and the robot’s own information. It can be represented as S=[Se,Sg,Sbot] . Here, Se represents the environmental point cloud data obtained from the LiDAR, Sg represents the target point information, and Sbot represents the robot’s state information.

#### 2. Action Space

the action space A consists of linear and angular velocity commands. It can be represented as A=[v,w] . Where v[0,0.2] (m/s), and w[−1,1] (rad/s).

#### 3. Reward Function

reward expressed as follows:

$$
r=
\begin{cases}
C_g, & \text{if goal reached}\\
C_c, & \text{if collision}\\
(r_d^{t-1}-r_d^{t})\cdot C_e, & \text{if distance is reduced}\\
-C_s, & \text{otherwise}
\end{cases}
\tag{3}
$$

where Cg,Cc,Ce , and Cs is a constant, and rdt−1 and rdt are the relative distances at times t−1 and t , respectively.

### D. EWC-Based CRL

EWC prevents the forgetting of neural network parameters learned from previous scenes by applying regularization. The core idea is to use the Fisher information matrix to measure the importance of parameters, thereby constraining the changes to important parameters.

Within the Bayesian inference framework, the posterior probability can be factorized as shown in the following equation:

$$
\log P(\theta\mid D)=\log P(D\mid\theta)+\log P(\theta)-\log P(D)
\tag{4}
$$

In continual learning, data comes from different scenes, so D can be partitioned into data from two independent scenes, T1(DT1) and T2(DT2) [18]. Based on this, rewriting (4) leads to the following equation:

$$
\log P(\theta\mid D)=\log P(D_{T_2}\mid\theta)+\log P(\theta\mid D_{T_1})-\log P(D_{T_2})
\tag{5}
$$

By omitting the normalization term, the posterior probability can be factorized as shown in the following equation:

$$
\log P(\theta\mid D)\propto \log P(D_{T_2}\mid\theta)+\log P(\theta\mid D_{T_1})
\tag{6}
$$

For the posterior probability logP(θ|D) , the Laplace approximation is used, assuming a Gaussian distribution with the mean being the optimal parameters θ∗T1 from the previous scene. The covariance matrix is determined by the inverse of the Fisher information matrix F , as shown in the following equation:

$$
\log P(\theta\mid D_1)\approx -\frac{1}{2}(\theta-\theta_{T_1}^{*})^{T}F(\theta-\theta_{T_1}^{*})+\epsilon
\tag{7}
$$

Thus, maximizing the posterior probability is equivalent to minimizing the loss function, as represented in the following equation:

$$
L(\theta)=L_{T_2}(\theta)+\frac{\lambda}{2}\sum_i F_i(\theta_i-\theta_{T_1,i}^{*})^2
\tag{8}
$$

Here, Fi represents the diagonal elements of the Fisher information matrix, and λ is the regularization coefficient. The Fisher information matrix F is used to measure the sensitivity of parameters to model predictions. For the model obtained after training on scenes k , its computation formula is given by the following equation:

$$
F_i=\mathbb{E}_{x\sim D_{T_k}}\left[
\left(\frac{\partial \log P(y\mid x,\theta)}{\partial \theta_i}\right)^2
\right]
\tag{9}
$$

where x represents the input, y represents the output, and the expectation is taken over the data from scenes Tk , with the Monte Carlo method used for estimation in practice.

For the DDPG algorithm, the policy network μ(s|θ) generates the final action. Therefore, during EWC regularization, it is sufficient to apply the regularization only to the parameters of the policy network. Since the output of the policy network is deterministic and the log-probability cannot be directly computed, we assume that the output action follows a Gaussian distribution, with the mean being μ(s|θ) , as shown in the following equation:

$$
a=\mu(s\mid\theta)+\epsilon,\qquad \epsilon\sim\mathcal{N}(0,\sigma^2)
\tag{10}
$$

Taking the logarithm of it results in the following equation:

$$
\log \pi(a\mid s)=
-\frac{(a-\mu(s\mid\theta))^2}{2\sigma^2}
-\frac{1}{2}\log(2\pi\sigma^2)
\tag{11}
$$

The gradient of it is as follows:

$$
\frac{\partial \log \pi(a\mid s)}{\partial \theta_i}
=
\frac{a-\mu(s\mid\theta)}{\sigma^2}\cdot
\frac{\partial \mu(s\mid\theta)}{\partial \theta_i}
\tag{12}
$$

Based on the above expression, the Fisher information approximation of the policy network for scene k is obtained as follows:

$$
F_{\mu}^{T_k,i}\approx
\mathbb{E}_{s\sim D_{T_k}}\left[
\left(\frac{\partial \mu(s\mid\theta)}{\partial \theta_i}\right)^2
\right]
\tag{13}
$$

In practice, the state S is sampled from the data of the previous scenes, and the average value of the squared gradient is calculated. By applying EWC regularization to the loss function of the policy network, the loss function for the policy network on scene Tk can be expressed as follows:

$$
L_{\mu}^{T_k}(\theta)=
-\mathbb{E}_{s\sim D_{T_k}}\left[Q_\omega(s,\mu(s\mid\theta))\right]
+\frac{\lambda}{2}\sum_i F_{\mu}^{T_{k-1},i}(\theta_i-\theta_{T_1,i})^2
\tag{14}
$$

For additional scenes, the Fisher matrix is accumulated through a discount factor, as shown in the following equation:

$$
F_{\mu}(T_k,i)=\lambda F_{\mu}(T_{k-1},i)+F_{\mu}(T_k,i)
\tag{15}
$$

### E. Knowledge-Guide CRL

Although the above methods prevent catastrophic forgetting, the strategies obtained from previous scenes are prone to getting stuck in local optima in new scenes due to the solidification of action features. Integrating external knowledge to guide the learning process can more effectively guide exploration and reduce the risk of suboptimal solutions. This section introduces three methods for integrating knowledge guidance into a framework. The goal is to combine these guidance techniques to improve the performance of the method.

#### 1. Exploration Mechanism

Based on the KGE strategy presented in [26], the action policy guided by external knowledge can be expressed as follows:

$$
a_G(a_{ks},a_{rl})=\theta_G a+(1-\theta_G)a_{ks}
\tag{16}
$$

Here, θG represents the fusion parameter, which changes with the update of the generalizer and determines the proportion of the policy network’s action output fused with the action output from the external knowledge. aks represents the action produced by the external knowledge strategy, and a represents the action produced by the policy network.

Through this guided exploration strategy, the agent interacts with the environment, generating a tuple ([s,aG,r,s′,aks] ) which is then stored in the experience pool. Using the collected tuple, the fusion parameter is updated with the help of the evaluation network Qω , and the objective function for this update is as follows:

$$
L_G^{T_k}(\theta_G)=-\mathbb{E}_{s\sim D_{T_k}}\left[Q_\omega(s,a_G)\right]
\tag{17}
$$

#### 2. Additional Reward

Building on the exploration mechanism mentioned above, the AR is defined as follows:

$$
r_g=(1-\theta_G)C_{gd}
\tag{18}
$$

#### 3. Learning Objective

Given the AR, the value network objective function LQTk is defined as follows:

$$
L_Q^{T_k}(\omega)=
\mathbb{E}_{s\sim D_{T_k}}\left[
\left(
Q_\omega(s,a)-
\left(r+r_g+\gamma\max_{a'}Q_{\bar{\omega}}(s',a')\right)
\right)^2
\right]
\tag{19}
$$

For the policy network, the external knowledge strategy can serve as a good reference. Therefore, the policy network objective function includes a behavioral cloning term to encourage the policy network to learn from the external knowledge strategy. This term is defined as (20). Here, α=(1−θG) .

$$
L_{\mu}^{T_k}(\theta)=
-\mathbb{E}_{s\sim D_{T_k}}\left[Q_\omega(s,\mu(s\mid\theta))\right]
+\frac{\lambda}{2}\sum_i F_{\mu}(T_{k-1},i)(\theta_i-\theta_{T_1,i})^2
+\alpha\cdot\frac{1}{N}\sum\left(\mu(s\mid\theta)-a_{ks}\right)^2
\tag{20}
$$

**Integration:** The KGCRL method integrates the above three guidance techniques, harnessing the power of external knowledge strategies. Algorithm 1 provides the overall procedure for the algorithm.

#### Algorithm 1. Knowledge-Guided Continual RL

```text
1. Given: Policy network μ(s|θ) with parameters θ , Qω(s,a) parameters ω , aG(aks,arl) parameters θG , empty replay buffer D
2. Set target parameters equal to main parameters: θ¯←θ , ϖ←ω
3. for scene =1,2,…,K do
4. reset buffer
5. for episode =1,2,…,M do
6. Observe initial state s
7. for t =1,2,…,T do
8. select action based on aG and execute
9. Store transition (st,at,rt,st+1,aks) in D
10. if time to update then
11. Sample a batch of transitions (si,ai,ri,s′i,aks,i) from D
12. Update Qω(s,a) , μ(s|θ) , aG(aks,aμθ) based on LQTk(ω) (Eq. 19), LμTk(θ) (Eq. 20), LGTk(θG) (Eq. 17), respectively.
13. Update target network with ϖ←ρϖ+(1−ρ)ω,θ←ρθ¯+(1−ρ)θ
14. end if
15. end for
16. end for
17. Record the current scene parameters θ∗Tk
18. calculate the Fisher matrix FμTk,i
19. end for
```

**Remark 4.** Across diverse research paradigms, the constitution of knowledge varies substantially, potentially encompassing environmental priors, demonstration datasets, pretrained networks, expert rules, as well as planning and control methodologies. In this work, the knowledge strategy combines a global planner (A∗ ) and a local controller (PID) to dynamically generate reference actions during training. Specifically, A∗ utilizes the simulated environment’s occupancy grid to compute an optimal path, while PID converts path waypoints into continuous control commands that serve as reference actions for the RL agent. These actions are integrated in real time through the knowledge-guided module, forming interactive guidance for policy learning. During real-world deployment, the learned policy operates without A∗ or a global map, relying solely on onboard sensory observations.
### F. Discussion on Method

In the DDPG algorithm, given a state dimension S and an action dimension A , the parameter sizes of the Actor and Critic networks are Nμ and NQ , respectively. The computational complexity of a single forward pass is O(Nμ+NQ) , while that of backpropagation remains O(Nμ+NQ) . For a training process with M sampled transitions per step over T steps, the overall computational complexity is O(TM(Nμ+NQ)) . In KGCRL, the computational complexity is influenced by external knowledge strategies and EWC. EWC primarily affects backpropagation by adding a regularization term FμTk−1,i(θi−θT1,i)2 , which incurs an additional cost of O(Nμ+NQ) . The Fisher matrix computation, requiring gradient evaluation over M1 samples, has a complexity of O(M1(Nμ+NQ)) . Thus, EWC increases the constant factor but does not alter the complexity order compared with DDPG.

The complexity of knowledge guidance depends on the form of the knowledge strategy. If the strategy is derived from a neural network with parameter size Nk , its forward inference complexity is O(TNk) . If rule-based or model-driven approaches are used, the additional computational cost is negligible. Therefore, KGCRL retains the same complexity order as DDPG while improving learning efficiency through knowledge-driven guidance.

In incremental scene navigation, revisiting previous data is infeasible due to the diverse and evolving environments, rendering experience replay and network expansion approaches unsuitable. To address this, we impose constraints on network parameter updates to enable continual learning without data replay. Knowledge strategies can be derived from neural networks, rule-based reasoning, or planning and control methods such as A∗ + PID. The completeness of the knowledge strategy directly affects its guidance effectiveness, making its careful design crucial for performance enhancement.

## IV. Experimental Validation

The proposed method leverages knowledge strategies to enhance RL agent performance in incremental scenes and improve continual learning via parameter constraints. Accordingly, the experiments aim to answer: 1) Can the method handle incremental scenes? 2) Does it demonstrate continual learning and mitigate catastrophic forgetting? 3) Is the knowledge strategy effective? This section provides a detailed description of the verification platform and setup.

### A. Baseline Methods

The baseline methods used for comparison are summarized as follows.

**DDPG [32] + Fine-Tuning:** A standard actor–critic method for navigation without knowledge guidance or continual learning, serving as a baseline.

**EWC [18]:** Adds EWC constraints to DDPG for continual learning, evaluating the impact of knowledge guidance on overcoming local optima.

**RGEWC-DDPG [26]:** Integrates EWC into a rule-based knowledge-guided DDPG framework, assessing the effectiveness of the proposed method over rule-based approaches.

**L2CRL [33]:** A regularization-based continual RL method as an advanced baseline for continual learning.

**KGL2CRL:** Added the knowledge guidance module of this article to explore the forgetting characteristics under deep learning for subsequent scenes.

### B. Implementation Details

#### 1. Training Scenes

Four training environments were designed to evaluate navigation and continual learning, as shown in Fig. 2. The first is an open space without obstacles. The second adds many obstacles, increasing complexity. The third alters obstacle positions and types to test adaptability to changing state distributions. The fourth starts the robot in a narrow, trapped space (red box), and evaluates the knowledge guidance. Each environment has a fixed start position and a random goal.

#### 2. Real-World Scenes

Two real-world environments were set up to validate the proposed method, as shown in Fig. 3. The first, an obstacle-rich environment different from the simulation, evaluates generalization to unseen conditions. The location and shape of obstacles in the second environment are different from the first, further evaluating the performance in real-world scenes. The robot used is turtlebot3 burger.

#### 3. Evaluation Metrics

The evaluation metrics used in this study are defined as follows.

**Forgetting:** Measures loss of earlier scene knowledge after training new scenes [34]. For scene Tk

$$
F(T_k)_i=A_i(T_i)-A_i(T_k),\qquad
F(T_k)=\frac{1}{k-1}\sum_{i=1}^{k-1}F(T_k)_i
\tag{21}
$$

Here, Ai(Ti) represents the success rate on scene Ti immediately after completing Ti , while Ai(Tk) reflects the success rate on scene Ti (i<k ) after learning scene Tk . A positive F(Tk) indicates forgetting, whereas a negative value implies the presence of backward knowledge transfer.

**Forward Transfer:** Evaluates how past knowledge aids learning of $T_k$.

$$
\mathrm{FWT}_k = \frac{1}{k-1}\sum_{i=1}^{k-1} A_k(T_i)
$$

$$
FT(T_k) = \frac{1}{k-1}\sum_{i=2}^{k} \mathrm{FWT}_k
\tag{22}
$$


**SASR:** Mean performance on each trained scene

$$
SASR=\frac{1}{k}\sum_{i=1}^{k}A_i(T_i)
\tag{23}
$$

**ASR:** Overall performance across all scenes

$$
ASR=\frac{1}{k^2}\sum_{i=1}^{k}\sum_{j=1}^{k}A_i(T_j)
\tag{24}
$$

#### 4. Network Model Construction

The proposed method is based on DDPG with an actor–critic architecture (see Fig. 4). The actor receives a 94-D state input comprising preprocessed point cloud data (replacing inf with 3.5 and nan with 0), target information, and previous linear and angular velocities and outputs linear and angular velocities using sigmoid and tanh activations. The critic takes a 96-D input (state + action), processes it via a fully connected layer with 128 neurons, and outputs the action value. The network is optimized using the Adam optimizer with hyperparameters shown in Table I.

> **Table I Parameter Settings.** *(Table body was not present in the copied text.)*

## V. Results and Analysis

### A. Incremental Scene Training Comparison

We trained across four sequential scenes, each in a distinct environment with no access to previous ones. Simpler scene (T1) required fewer episodes (500), while more complex scenes (T2–T4) used 1000 episodes. Fig. 5 shows ASRs, with color blocks indicating scene intervals. In Fig. 5(a), DDPG performs well in T1. However, performance drops in T2 due to obstacles invalidating prior strategies and insufficient exploration. T3 benefits from similarities to T2, but random exploration limits progress. In T4, DDPG had zero success, which can be seen from the Gazebo training process that this is because random exploration cannot make it escape the narrow space, making it unable to converge in the set training round.

As shown in Fig. 5(b), the DDPG + EWC method exhibits comparable performance to DDPG in T1, but shows improvement in T3. This is because the combination of EWC constraints enables agents to better retain and transfer knowledge in T2, thereby promoting more effective learning in T3. However, in T4, both DDPG + EWC and DDPG were unable to adapt to significant environmental changes, resulting in a success rate close to zero.

In conclusion, the proposed method demonstrates strong adaptability and learning capabilities, effectively improving performance in incremental scenes and complex environments.

### B. Qualitative Analysis of Forgetting Characteristics

To analyze the forgetting characteristics, we compared model performance across different scenes by evaluating models trained up to T1 through T4 on their corresponding and prior scenes. For example, the model after T3 was tested on T3, T2, and T1, allowing us to assess knowledge forgetting. A significant decline in performance on earlier scenes indicates greater forgetting.

To analyze the relationship between forgetting behavior and training level, models of KGCRL with different training steps on T4 were evaluated, and each model was tested for 100 rounds on T1–T4. As shown in Fig. 8, the performance of the model on T4 improves with increasing training, with the number of successful steps increasing from 0 in 3000 steps to 74 in 28 000 steps. This indicates a positive correlation between training depth and performance in the current scene. In contrast, in the previous scene, the performance significantly decreased: as the number of training iterations increased, the success rate of T2 decreased from 76 to 52, and T3 decreased from 61 to 27. These results indicate that more intensive training on the current scene leads to greater forgetting of previously learned scenes, revealing a tradeoff between task-specific optimization and overall knowledge retention.

In summary, as scene number and dissimilarity increase, forgetting becomes inevitable, with deeper learning of subsequent scenes leading to more forgetting of earlier scenes. However, the proposed method using EWC effectively mitigates forgetting, with manageable rather than catastrophic loss of prior scene performance. The approach outperforms alternative methods across multiple scenes.

### C. Quantitative Analysis of Sequential Scene Performance

As shown in Table II, all methods exhibit catastrophic forgetting to varying degrees. For example, KGL2CRL achieves a success rate of 0.61 on T2 immediately after training on MT2, which then drops to 0.57 after MT3 and further to 0.37 after MT4. A similar trend is observed on T3, where the performance declines from 0.44 (MT3) to 0.34 (MT4). The forgetting metric FTk also reflects an increasing forgetting rate as training progresses, with KGL2CRL rising from 0.0 (FT2 ) to 0.113 (FT3 ). In contrast, KGCRL demonstrates better resistance to forgetting, with only minor performance degradation. For instance, on T1, the success rate drops slightly from 1.00 (MT3) to 0.97 (MT4). For T2, the performance decreases from 0.68 (MT2) to 0.66 (MT4). Interestingly, a negative value is observed for FT2 (−0.02), indicating a facilitation effect rather than forgetting. Furthermore, FT3 is also lower than that of KGL2CRL, suggesting that KGCRL provides superior resistance to forgetting compared with L2CRL. The forward-transfer metric further indicates that both KGCRL and KGL2CRL possess positive forward transfer capabilities. However, KGCRL exhibits slightly lower values, likely due to its stronger protection of task-specific parameters. This conservative strategy sacrifices some forward transferability in exchange for reduced forgetting. Moreover, KGCRL outperforms KGL2CRL in both SASR and ASR metrics, reflecting better scene-specific and overall performance.

> **Table II Performance After Training Each Scene.** *(Table body was not present in the copied text.)*

### D. Ablation

An ablation study was conducted to assess the impact of different knowledge components on the agent’s performance. By systematically removing components such as the knowledge-guided (KG), KGE, AR, and knowledge-guided objective (KOB), success rates were measured across 250 episodes for T1 and 500 episodes for subsequent scenes. The results, normalized against the proposed method, showed that removing knowledge guidance severely hindered exploration, especially in narrow spaces where the agent got stuck in local optima. Removing KGE affected data collection, though KOB maintained some success. The absence of AR resulted in an average decrease of 9.6% in success rate (average cumulative reduction per block), while removing KOB led to a decrease of 66.5%, highlighting its crucial role in parameter updates and policy formation. Overall, the study demonstrates the significant contribution of each knowledge component to the agent’s learning, especially in complex environments.

### E. Analysis of Knowledge Source Strategies

To further examine the influence and generalization of different knowledge sources, we conduct additional experiments by varying only the knowledge provider while keeping other configurations unchanged. The compared strategies include: 1) A∗+PID , used in our main method (KGCRL); 2) RG (Rule-Guided), a fuzzy-rule-based system with four navigation rules (if the goal is on the left, then turn left; if the obstacle distance is below a threshold, then stop); and 3) NETG-1 and NETG-2, two pretrained policy networks with different training quality, where NETG-1 is undertrained and NETG-2 is better optimized.

The results in Fig. 10 demonstrate that the quality and relevance of the knowledge source have a significant impact on learning. High-quality knowledge (NETG-2) accelerated convergence in scene T4, while low-quality knowledge (NETG-1) produced negligible or even slightly adverse effects. The RG method provided a weak improvement due to its limited rule coverage and inability to handle complex scenarios. By contrast, A∗+PID offered more consistent and informative guidance across tasks, which contributed to stable policy learning and reduced negative transfer. These findings highlight that the proposed KG module is flexible and that its effectiveness is related to the quality of external knowledge. These results indicate that the proposed KG framework is flexible and can accommodate various types of external knowledge. However, its performance is inherently linked to the reliability and coverage of the knowledge sources. In dynamic or unstructured environments, A∗+PID cannot provide accurate reference actions, and the guidance effect may be weakened, but knowledge sources capable of handling dynamic or unstructured environments can also be integrated. To further examine the impact of poor guidance, we conducted an extreme case experiment in which the external policy was replaced by a constant “turning-in-place” behavior shown in Fig. 11. When trained in Env1, the resulting performance was even worse than that of the baseline DDPG, confirming that inadequate or misleading knowledge can indeed harm the RL process.

**Remark 5.** These findings show that knowledge guidance is helpful only when its quality is reliable; low-quality knowledge can cause negative transfer. While its influence can be reduced by assigning a smaller initial fusion weight, automatic detection of unreliable knowledge is not supported in the current framework.

### F. Sim to Real

To validate the feasibility of the proposed method in real-world scenes, experiments were conducted in two different scenes. The results are as follows.

#### 1. Experiment 1

The experimental setup is illustrated in Fig. 3(a), where the environment differs from the training setting in terms of field size, as well as the size, shape, and distribution of obstacles. The selected target points are presented in Table III. Fig. 12(a) depicts the actual movement of the mobile robot, while Fig. 12(b) illustrates the complete trajectory.

> **Table III Target for Experiment 1.** *(Table body was not present in the copied text.)*

From Fig. 12(b), it can be observed that the DDPG algorithm successfully reached the second and fourth target points, both of which are simple, unobstructed locations. The DDPG + EWC method achieved the same performance as DDPG, reaching only the second and fourth target points. Similarly, the RGEWC-DDPG method exhibited a comparable performance to these two approaches. L2CRL reaches one point more than the previous method. In contrast, the proposed method demonstrated superior performance, with only a single collision occurring at the final target point. The lower success rates of the first three methods can be attributed to their inadequate obstacle avoidance capabilities. Notably, the trajectory of the proposed method reveals that it follows a larger turning radius, which facilitates better obstacle avoidance.

#### 2. Experiment 2

To further evaluate the real-world performance of different methods, a second experiment was conducted in an environment with a higher density of obstacles compared with Experiment 1. The experimental setup is depicted in Fig. 3(b), and the five selected target points for testing are listed in Table IV. Fig. 13(a) presents the actual trajectories corresponding to these target points, while the complete recorded trajectories for all methods are shown in Fig. 13(b).

> **Table IV Target for Experiment 2.** *(Table body was not present in the copied text.)*

As seen in Fig. 13(b), the DDPG method successfully reached the fourth and fifth target points. However, similar to Experiment 1, it struggled with obstacle avoidance at the remaining points, indicating that the DDPG model possesses only basic navigation capabilities. This limitation can be attributed to poor generalization, as the real-world environment exhibits significant differences from the training setting. Moreover, during continual learning, DDPG failed to effectively acquire navigation skills suited for complex, obstacle-dense environments. The DDPG + EWC method successfully reached three target points. However, for target points positioned behind obstacles, the robot correctly oriented itself but failed to navigate around the obstacles. L2CRL and RGEWC-DDPG have only reached two target points. Notably, the trajectory of RGEWC-DDPG was observed to be significantly straighter compared with other methods, closely resembling rule-based behaviors. This suggests that the model successfully learned rule-based strategies during training. However, due to insufficient exploration of the complex environment, it failed to obtain a more comprehensive set of behavioral characteristics. In contrast, the proposed KGCRL method demonstrated a clear advantage over all other approaches, successfully reaching all target points. Moreover, it exhibited superior obstacle avoidance capabilities compared with other methods.

The overall experimental results indicate that the model trained using the proposed method outperforms the baseline methods in real-world environments. This generalization ability can be attributed to the continual learning mechanism and the effective incorporation of external knowledge, enabling the model to adapt more efficiently to complex navigation scenes.

#### 3. Experiment Quantitative Analysis

To provide a more objective evaluation of real-world performance, quantitative results (mean and standard deviation) of trajectory length (Len) and completion time for five target points repeated three times in two environments are summarized in Table V. The symbol “−” indicates that the agent failed to reach the target, Pi is Point-i . As shown, KGCRL achieves the highest overall task completion rate, successfully reaching nearly all targets where other methods failed. Although its trajectories are not always the shortest or fastest, this reflects a tradeoff in favor of stability and success reliability. The balance between efficiency and robustness was not emphasized in this article and will be further explored in future work.

> **Table V Quantitative Results in Real-World Environments (Len in Meters, Time in Seconds). “−” Indicates Task Failure.** *(Table body was not present in the copied text.)*

## VI. Conclusion

This article explores how to enhance the continual learning ability of RL agents by leveraging external knowledge to guide the learning process, thereby improving adaptability and generalization in incremental scenes. The research extends the existing DDPG framework to a continual learning setting, enabling agents to sequentially learn across multiple scenes without relying on joint training, while retaining the capacity for continual expansion to new scenes. Experimental results demonstrate that incorporating the EWC mechanism allows agents to preserve previously acquired knowledge without dependence on historical scene data, thereby strengthening their adaptability to incremental scenes. Moreover, the multidimensional utilization of external knowledge strategies effectively alleviates the constraints of policy consolidation during continual learning, mitigates the hindrance to learning new scenes, and enhances exploration efficiency. Although regularization-based approaches facilitate knowledge retention under constrained conditions, they cannot fully eliminate catastrophic forgetting. Exploring more flexible and multiperspective strategies beyond these limitations represents a promising direction for future research, including mechanisms for assessing and down-weighting low-quality or unreliable knowledge.

---

## Conversion Notes

- Figures and duplicated IEEE figure-display blocks were excluded as requested.
- Table captions are retained only as notes where the copied text did not include the table body.
- All numbered equations visible in the pasted source were converted into LaTeX display math.
- Equation (22) was corrected using the screenshot provided in the chat.
- Reference numbers from the original text, such as `[1]`, are preserved, but the reference list was not included in the copied source.
