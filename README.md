# THEFENCEBOT 🤺

A real-time teleoperation simulation system for a custom 6-DOF robotic arm. Pose commands are streamed over UDP to an Isaac Lab simulation where a differential IK solver computes and executes joint trajectories in real time.

## 🎯 Project Overview

THEFENCEBOT is a simulation-first teleoperation framework for the ASEM V2 robotic arm. The current implementation focuses on the Isaac Lab simulation layer: receiving 6-DOF pose targets over UDP, solving inverse kinematics using a damped least squares controller, and driving the arm to track the target in real time.

The longer-term goal is to close the loop with a real VR headset and deploy to physical hardware.

**Current Status:** Isaac Lab simulation + IK tracking working. ROS2 middleware pipeline planned but not yet implemented.

---

## System Architecture

### Implemented (Working)

```
Test Script / VR Emulator
    │
    │  UDP packets (x, y, z, qx, qy, qz, qw) — 28 bytes
    │  Port 5006
    ▼
Isaac Lab (Python 3.11)
    │  UDPListener thread (non-blocking)
    │  Differential IK solver (DLS, λ=0.1)
    │  Joint position targets → PhysX
    ▼
Isaac Sim 5.1
    │  6-DOF ASEM arm at 100Hz
    └  RTX Real-Time viewer
```

### Planned (Not Yet Implemented)

```
VR Headset
    │  UDP Port 5005
    ▼
ROS2 C++ Node: vr_udp_publisher  →  /vr_pose topic
    ▼
ROS2 C++ Node: robot_controller  →  UDP Port 5006
    ▼
Isaac Lab (same as above)
```

---

## Project Structure

```
THEFENCEBOT/
├── isaac_env/
│   ├── vr_arm_env.py        # ASEM DirectRLEnv + actuator config
│   └── run_sim.py           # UDP listener + IK controller loop
│
├── src/
│   └── vr_robot_sim/        # ROS2 C++ package (planned)
│       ├── src/
│       │   ├── vr_udp_publisher.cpp
│       │   └── robot_controller.cpp
│       ├── CMakeLists.txt
│       └── package.xml
│
├── Simulation/
│   └── ASEM_V2.SLDASM/
│       ├── urdf/
│       │   └── ASEM_V2.SLDASM.urdf
│       └── usd/
│           └── ASEM_V2.usd       # Isaac Lab asset
│
├── Math/
│   └── 6dof_math_mode.ipynb      # Kinematics derivations
│
├── IsaacLab/                     # Isaac Lab v2.3.2 install
└── README.md
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Simulation | Isaac Lab 2.3.2 + Isaac Sim 5.1 |
| IK Solver | DifferentialIKController — damped least squares |
| Physics | PhysX (via Isaac Sim) |
| Communication | UDP sockets (28-byte float packets) |
| Robot | ASEM V2 — 6-DOF custom arm |
| Python | 3.11 (Isaac Lab venv) |
| Planned middleware | ROS2 Humble, C++17 |

---

## 🤖 Robot Specs (ASEM V2)

| Property | Value |
|----------|-------|
| DOF | 6 |
| Joint names | j1, j2, j3, j4, j5, j6 |
| Joint type | Revolute |
| Joint limits | ±π rad |
| End effector | link6 |
| Rest position (EE) | [0.573, -0.025, 0.582] m |
| Actuator stiffness | 800.0 |
| Actuator damping | 40.0 |

---

## IK Solver

The IK uses Isaac Lab's `DifferentialIKController` configured as follows:

```python
DifferentialIKControllerCfg(
    command_type="pose",           # full 7-DOF: position + quaternion
    use_relative_mode=False,       # output is absolute joint positions
    ik_method="dls",               # damped least squares
    ik_params={"lambda_val": 0.1}  # singularity damping factor
)
```

**Why DLS:** The ASEM arm encounters kinematic singularities (rank-deficient Jacobian) at certain configurations. Plain pseudoinverse causes oscillation at these points. Damped least squares regularizes the solution, trading a small tracking error (~0.02–0.05m near singularities) for stability.

**Jacobian:** Full 6×6 slice from PhysX — `get_jacobians()[:, ee_idx-1, :6, :6]` — covering all 6 joints and both translational and rotational rows.

**Frame:** EE pose passed to the controller is in robot root frame (`body_pos_w - root_pos_w`).

---

## 🚀 Setup

### Prerequisites

- Ubuntu 22.04
- NVIDIA GPU (8GB+ VRAM, driver 525+)
- CUDA 12.x
- Python 3.11
- Isaac Lab 2.3.2 installed at `/opt/isaaclab_data/.venv`

### Environment

```bash
# Activate Isaac Lab venv
source /opt/isaaclab_data/.venv/bin/activate

# Convenience alias (add to ~/.bashrc)
alias simenv='source /opt/isaaclab_data/.venv/bin/activate'
```

---

## ▶️ Running the Simulation

**Terminal 1 — Isaac Lab Sim**
```bash
simenv
cd ~/THEFENCEBOT/isaac_env
~/THEFENCEBOT/IsaacLab/isaaclab.sh -p run_sim.py
```

**Terminal 2 — Send test poses**

Static target:
```bash
python3 -c "
import socket, struct, time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = struct.pack('7f', 0.5, 0.0, 0.6, 0.0, 0.0, 0.0, 1.0)
    sock.sendto(data, ('127.0.0.1', 5006))
    time.sleep(0.02)
"
```

Circle sweep (IK tracking test):
```bash
cat > /tmp/send_pose.py << 'EOF'
import socket, struct, time, math
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t = 0.0
while True:
    x = 0.5 + 0.1 * math.cos(t)
    y = 0.1 * math.sin(t)
    z = 0.6
    qx, qy, qz, qw = 0.0, 0.0, 0.0, 1.0
    data = struct.pack('7f', x, y, z, qx, qy, qz, qw)
    sock.sendto(data, ('127.0.0.1', 5006))
    t += 0.005
    time.sleep(0.02)
EOF
python3 /tmp/send_pose.py
```

---

## 📊 UDP Packet Format

```
[ x | y | z | qx | qy | qz | qw ]
  4   4   4    4    4    4    4    = 28 bytes (7 × float32)
```

Position in meters. Quaternion in `(qx, qy, qz, qw)` — reordered to `(qw, qx, qy, qz)` internally before passing to the IK controller.

---

## Current Progress

- [x] ASEM URDF → USD conversion
- [x] ASEM arm spawning in Isaac Sim
- [x] UDP pose listener (threaded, non-blocking)
- [x] Differential IK solver — full pose (position + orientation)
- [x] DLS singularity handling
- [x] Real-time EE tracking via circle sweep test
- [ ] ROS2 C++ UDP publisher node
- [ ] ROS2 C++ robot controller node
- [ ] VR headset integration
- [ ] Workspace scaling (VR space → robot workspace)
- [ ] Gripper control
- [ ] Hardware deployment

---

## Known Issues / Notes

- ROS2 Humble (Python 3.10) and Isaac Lab (Python 3.11) cannot share a process — middleware communication will use UDP rather than rclpy
- Target positions should stay within ~0.1–0.15m of [0.5, 0.0, 0.6] for reliable IK convergence
- DLS tracking error near singularities is expected behavior, not a bug

---

## License

MIT License

---

**Last Updated:** March 2026