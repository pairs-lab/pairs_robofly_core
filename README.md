# pairs_robofly_core

Support and integration resources for the F4F Robofly, a small camera-equipped multirotor running the PAIRS UAV stack. The repository bundles the ROS package that wires the Robofly's onboard sensors (IMU, downward camera) into PAIRS estimation and control, together with the Docker Compose sessions and host setup used to deploy and simulate the platform.

## Contents

- `pairs_robofly_core` — Robofly platform package: launch files for visual-inertial odometry (`open_vins.launch`, `vins_republisher.launch`) and the per-airframe `platform_config.yaml` (motor thrust curve, estimator/controller/tracker tuning).
- `pairs_robofly_example` — minimal `rospy` example node (`robofly_example.py`) that streams a trajectory to the control manager and lands the drone, useful as a flight-control template.
- `docker/` — Compose sessions for the drone (VIO and GNSS UAV systems, camera and sensor diagnostics, Nimbro network link, Hailo AI/YOLO) and a local Gazebo simulation session for the Robofly.
- `setup/` — host bring-up helpers (Portainer agent/server, local Docker registry).

## Install (ROS 1 Noetic)

```bash
sudo apt install ros-noetic-pairs-robofly-core
```

## Usage

Bring up Robofly visual-inertial odometry (requires `UAV_NAME` to be set):

```bash
roslaunch pairs_robofly_core open_vins.launch
```

Run the example trajectory node:

```bash
roslaunch pairs_robofly_example robofly_example.launch
```

Launch the local Gazebo simulation session:

```bash
cd docker/simulation && ./up.sh
```
