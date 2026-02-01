# Term Project Proposal: VR Teleoperated Fencing Robot

## Project Title
**Teleoperation and Trajectory Optimization for High-Speed Robotic Manipulation: A Fencing Application**

---

## Problem Statement

High-speed manipulation tasks such as robotic fencing require real-time inverse kinematics, trajectory optimization, and human-in-the-loop control with minimal latency. This project investigates the computational and control challenges of mapping human motion from Virtual Reality (VR) to a robotic manipulator for dynamic fencing movements, with the goal of collecting demonstration data for future reinforcement learning applications.

**Key Research Questions:**
1. How can inverse kinematics be computed in real-time (<50ms) for dynamic manipulation tasks?
2. What trajectory optimization methods ensure smooth, collision-free sword movements during teleoperation?
3. How does VR-based human demonstration translate to robotic joint space through forward and inverse dynamics?
4. Can teleoperated demonstration data serve as a foundation for imitation learning and reinforcement control?

---

## Objectives

### Primary Objectives (2.5 months)
1. **Inverse Kinematics Implementation**: Develop and evaluate real-time IK solvers (analytical, numerical, MoveIt2) for 6/7-DOF robotic arm
2. **Forward and Inverse Dynamics**: Compute joint torques and velocities from VR controller inputs using robot dynamic models
3. **Trajectory Optimization**: Compare methods (quintic splines, minimum jerk, RRT) for smooth sword trajectories in constrained workspace
4. **Teleoperation Framework**: Build VR-to-robot pipeline with UDP communication, coordinate transformation, and safety constraints
5. **Data Collection**: Record synchronized VR inputs, robot states, and trajectories for future learning applications

### Secondary Objectives (If time permits)
6. **Behavior Cloning**: Train neural network on teleoperation data to replicate basic fencing movements
7. **Reinforcement Learning Foundation**: Set up simulation environment (MuJoCo/PyBullet) for RL training
8. **Trajectory Comparison**: Evaluate human demonstrations vs. optimized trajectories (energy, smoothness, task completion)

---

## Approach

### Phase 1: Kinematics and Dynamics (Weeks 1-4)
**Inverse Kinematics:**
- Implement analytical IK for 6-DOF arm (if closed-form solution exists)
- Numerical IK using Jacobian pseudoinverse with damped least squares
- Integrate MoveIt2 for comparison and singularity handling
- Benchmark computation time and accuracy

**Forward and Inverse Dynamics:**
- Derive equations of motion using Recursive Newton-Euler Algorithm
- Compute required joint torques for desired end-effector forces (e.g., sword contact)
- Validate against physics simulation (MuJoCo, PyBullet)

### Phase 2: Trajectory Optimization (Weeks 3-6)
**Methods to Compare:**
1. **Quintic Spline Interpolation**: Standard trajectory generation with boundary conditions
2. **Minimum Jerk Trajectory**: Optimize for smoothness (human-like motion)
3. **Direct Collocation**: Constrained optimization with workspace limits and velocity bounds
4. **RRT/RRT***: Sampling-based planning for obstacle avoidance

**Evaluation Metrics:**
- Computation time (real-time feasibility)
- Smoothness (jerk, acceleration continuity)
- Energy efficiency (integral of torque squared)
- Task success rate (target reaching accuracy)

### Phase 3: Teleoperation System (Weeks 4-8)
**VR Interface:**
- Unity + SteamVR for hand tracking
- UDP socket for low-latency streaming (target <50ms)
- Coordinate frame transformation (VR space → robot base frame)

**ROS2 Control Pipeline:**
```
VR Controller → UDP → ROS2 Bridge → IK Solver → Trajectory Optimizer → Motor Control
                                        ↓
                                  Safety Monitor
                                  (Workspace, Velocity, Singularity)
```

**Safety Systems:**
- Workspace boundaries (Cartesian limits)
- Joint velocity and acceleration limits
- Singularity avoidance (condition number monitoring)
- Emergency stop with latency <10ms

### Phase 4: Data Collection and Learning Foundation (Weeks 7-10)
**Data Recording:**
- VR controller poses (position, orientation, button states)
- Robot joint states (angles, velocities, torques)
- End-effector trajectories and contact forces (if force sensor available)
- Opponent sword position (if vision tracking implemented)

**Imitation Learning Setup:**
- Label demonstration data (attack types: thrust, cut, parry)
- Train simple behavior cloning model (MLP or LSTM)
- Compare robot execution to human demonstration (DTW distance)

**Simulation Environment (Optional):**
- Model robot and fencing sword in MuJoCo/PyBullet
- Transfer control policies from real robot to simulation
- Evaluate sim-to-real gap for future RL training

---

## Technical Components

### Computation
- **Inverse Kinematics**: Analytical (if possible), numerical (Jacobian-based), MoveIt2
- **Trajectory Optimization**: Quintic splines, minimum jerk, direct collocation, sampling-based
- **Real-time Control**: 100Hz+ control loop, multi-threaded architecture
- **Data Analysis**: Trajectory metrics, latency profiling, kinematics accuracy

### Software Stack
- **ROS2 Humble**: Middleware for control and communication
- **MoveIt2**: Motion planning and IK solving
- **Unity + SteamVR**: VR interface and teleoperation
- **Python/C++**: Node implementation
- **PyTorch/TensorFlow**: Machine learning (if time permits)
- **MuJoCo/PyBullet**: Physics simulation

### Hardware
- 6/7-DOF robot arm (UR5, Franka Emika, or similar)
- VR headset and controllers (Quest 3, Valve Index)
- Force/torque sensor (optional, for contact dynamics)
- Camera (optional, for opponent tracking)

---

## Expected Outcomes

### Deliverables
1. **Working teleoperation system** with real-time VR control of robotic arm
2. **Comprehensive kinematics analysis**: 
   - IK solver comparison (accuracy, speed, robustness)
   - Forward/inverse dynamics validation
3. **Trajectory optimization study**:
   - Comparison of 3+ methods
   - Performance benchmarks (computation time, smoothness, energy)
4. **Demonstration dataset**:
   - 10+ hours of labeled teleoperation data
   - Synchronized VR inputs and robot states
5. **Technical report and presentation**:
   - Literature review of manipulation control methods
   - Experimental results and analysis
   - Future work: RL policy learning

### Potential Extensions (Beyond 2.5 months)
- **Reinforcement Learning**: Train autonomous fencing policy using PPO/SAC
- **Opponent Modeling**: Vision-based tracking and predictive control
- **Human-Robot Competition**: User study comparing teleoperation vs. autonomous mode
- **Multi-Robot Coordination**: Two robots sparring autonomously

---

## Relation to Course Topics

This project directly addresses multiple course themes:

| Course Topic | Project Application |
|--------------|---------------------|
| **Inverse Kinematics** | Real-time IK for 6/7-DOF arm, singularity handling |
| **Forward Dynamics** | Torque computation from desired trajectories |
| **Inverse Dynamics** | Computing required actuator forces for contact tasks |
| **Trajectory Optimization** | Comparison of spline, optimization-based, and sampling methods |
| **Feedback Control** | Real-time VR-to-robot control loop, error correction |
| **Reinforcement Learning** | Data collection and foundation for future RL policies |
| **Computation** | Real-time constraints, optimization algorithms, GPU acceleration potential |

---

## Timeline (10 Weeks)

| Week | Milestone |
|------|-----------|
| 1-2 | VR-UDP-ROS2 pipeline, basic IK implementation |
| 3-4 | Dynamics modeling, trajectory optimization methods |
| 5-6 | Safety systems, teleoperation polish, data logging |
| 7-8 | Data collection, trajectory analysis, benchmarking |
| 9 | Behavior cloning experiments (if time permits) |
| 10 | Report writing, presentation preparation, demo |

---

## Success Metrics

**Minimum Viable Project:**
- ✅ Real-time teleoperation with <100ms latency
- ✅ At least 2 IK methods compared
- ✅ At least 2 trajectory optimization methods compared
- ✅ Recorded demonstration dataset
- ✅ Technical report with kinematics/dynamics analysis

**Stretch Goals:**
- ✅ <50ms latency
- ✅ Force sensing and contact dynamics
- ✅ Trained behavior cloning model
- ✅ Simulation environment for validation

---

## References (Preliminary)

1. Kelly, M. (2017). "An Introduction to Trajectory Optimization: How to Do Your Own Direct Collocation." *SIAM Review*, 59(4), 849-904.

2. Siciliano, B., et al. (2010). *Robotics: Modelling, Planning and Control*. Springer. (IK/Dynamics)

3. Ratliff, N., et al. (2009). "CHOMP: Gradient Optimization Techniques for Efficient Motion Planning." *ICRA*.

4. Argall, B. D., et al. (2009). "A Survey of Robot Learning from Demonstration." *Robotics and Autonomous Systems*, 57(5), 469-483.

5. OpenAI et al. (2018). "Learning Dexterous In-Hand Manipulation." *arXiv preprint*.

---

## Conclusion

This project provides a comprehensive exploration of manipulation control, combining classical robotics (kinematics, dynamics, trajectory optimization) with modern approaches (VR teleoperation, imitation learning). The fencing application offers unique challenges in high-speed, dynamic manipulation while producing valuable demonstration data for future reinforcement learning research.

---

**Project Category:** [Computation + Experiments (if hardware available)]

**Student Name:** [Pavan Kushal Velagaleti , Jordan irgang]  
**Date:** February 2026  
**Advisor/Instructor:** [Prof. Joo H.kim]