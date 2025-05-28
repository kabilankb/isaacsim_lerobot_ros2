
# Isaac Sim LeRobot ROS2 Bridge Example

This repository demonstrates how to set up and control a custom robot (LeRobot) in NVIDIA Isaac Sim 4.5 using the Python API, with ROS2 bridge integration for joint state publishing and command subscription.

---

## Features

- Loads a custom robot USD (`lerobot.usd`) and a simple room environment.
- Sets up an Action Graph for ROS2 communication (joint states, commands, and clock).
- Example for both GUI and headless simulation.
- Compatible with Isaac Sim 4.5 and ROS2 (e.g., Humble).

---

## Requirements

- [NVIDIA Isaac Sim 4.5](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html)
- [ROS2 Humble](https://docs.ros.org/en/humble/Installation.html) (or compatible)
- Python 3.10
- All dependencies required by Isaac Sim

---
![Image](https://github.com/user-attachments/assets/64e7799e-a51f-479e-81bc-f0e25cb4952b)
                         - Python standlone 

                         
## Usage

### 1. Clone the repository

```sh
git clone git@github.com:kabilankb/isaacsim_lerobot_ros2.git
cd isaacsim_lerobot
```

### 2. Place your robot USD

Make sure your robot USD file is at:
```
src/isaacsim_lerobot/lerobot.usd
```

### 3. Run the script

**From the terminal (headless or GUI):**
```sh
cd src/isaacsim_lerobot
python isaaclerobot.py
```

**From Isaac Sim Script Editor:**
- Open Isaac Sim.
- Open `src/isaacsim_lerobot/isaaclerobot.py` in the Script Editor.
- Press "Run".

### 4. ROS2 Bridge

- Make sure you have sourced your ROS2 environment:
  ```sh
  source /opt/ros/humble/setup.bash
  ```
- The script will publish joint states to `/so_100_arm_joint_states` and subscribe to `/so_100_arm_joint_commands`.

---

## File Structure

```
    └── isaacsim_lerobot/
        ├── isaaclerobot.py
        └── lerobot.usd
```

---

## Learn More

For a detailed step-by-step guide and explanation, **read this Medium article**:  
[Setting up LeRobot using API Standalone Method in NVIDIA Isaac Sim](https://medium.com/@kabilankb2003/setting-up-lerobot-using-api-standalone-method-in-nvidia-isaac-sim-f2b57164b0f2)

---

## Notes

- Update the USD paths in `isaaclerobot.py` if your files are in different locations.
- Make sure the required Isaac Sim extensions are enabled.
- For troubleshooting ROS2 bridge errors, ensure your ROS2 installation is sourced and the correct RMW implementation is installed.

---

## License

This project is for educational and research purposes only. See NVIDIA Isaac Sim EULA for details.
```
