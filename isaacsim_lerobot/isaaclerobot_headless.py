import sys
import numpy as np

import carb
import omni.graph.core as og
import usdrt.Sdf
from isaacsim.core.api import SimulationContext
from isaacsim.core.utils import extensions, prims, rotations, stage, viewports
from isaacsim.storage.native import get_assets_root_path
from pxr import Gf

# Define paths for your robot and background
ROBOT_STAGE_PATH = "/World/SO_5DOF_ARM100_8j_URDF_SLDASM"
ROBOT_USD_PATH = "/home/ubuntu/isaacsim_lerobot/src/isaacsim_lerobot/lerobot.usd"
BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_PATH = "/Isaac/Environments/Simple_Room/simple_room.usd"
ROOT_JOINT_PATH = "/World/SO_5DOF_ARM100_8j_URDF_SLDASM/root_joint"

# Enable required extensions for Isaac Sim 4.5+
extensions.enable_extension("isaacsim.ros2.bridge")
extensions.enable_extension("isaacsim.core.nodes")

simulation_context = SimulationContext(stage_units_in_meters=1.0)

# Get assets root path for loading USDs
assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets root path. Please check your Isaac Sim installation.")
    sys.exit()

# Optionally set camera view
viewports.set_camera_view(eye=np.array([1.2, 1.2, 0.8]), target=np.array([0, 0, 0.5]))

# Add background to the stage
stage.add_reference_to_stage(assets_root_path + BACKGROUND_USD_PATH, BACKGROUND_STAGE_PATH)

# Create the robot prim
prims.create_prim(
    ROBOT_STAGE_PATH,
    "Xform",
    position=np.array([0, -0.64, 0]),
    orientation=rotations.gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 0, 1), 90)),
    usd_path=ROBOT_USD_PATH,
)

# Action Graph Setup for ROS 2 Communication
try:
    og.Controller.edit(
        {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: [
                ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),
                ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                ("ROS2Context", "isaacsim.ros2.bridge.ROS2Context"),
                ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
                ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
                ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
                ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnImpulseEvent.outputs:execOut", "PublishJointState.inputs:execIn"),
                ("OnImpulseEvent.outputs:execOut", "SubscribeJointState.inputs:execIn"),
                ("OnImpulseEvent.outputs:execOut", "PublishClock.inputs:execIn"),
                ("OnImpulseEvent.outputs:execOut", "ArticulationController.inputs:execIn"),
                ("ROS2Context.outputs:context", "PublishJointState.inputs:context"),
                ("ROS2Context.outputs:context", "SubscribeJointState.inputs:context"),
                ("ROS2Context.outputs:context", "PublishClock.inputs:context"),
                ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
                ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
                ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
                ("SubscribeJointState.outputs:positionCommand", "ArticulationController.inputs:positionCommand"),
                ("SubscribeJointState.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),
                ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("ArticulationController.inputs:robotPath", ROBOT_STAGE_PATH),
                ("ArticulationController.inputs:rootJointPath", ROOT_JOINT_PATH),
                ("PublishJointState.inputs:topicName", "so_100_arm_joint_states"),
                ("SubscribeJointState.inputs:topicName", "so_100_arm_joint_commands"),
                ("PublishJointState.inputs:targetPrim", [usdrt.Sdf.Path(ROBOT_STAGE_PATH)]),
            ],
        },
    )
except Exception as e:
    print(e)

simulation_context.initialize_physics()
simulation_context.play()

# No simulation_app loop needed; Isaac Sim app manages the main loop.
# If you want to step manually, you can do:
# simulation_context.step(render=True)