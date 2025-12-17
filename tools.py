import numpy as np
from numpy.typing import ArrayLike
# Assuming your original file is named crs_robot.py
from crs_robot import CRSRobot

class CRSRobotWithTool(CRSRobot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define the tool offset: 0.135m in X-direction of the flange
        self.tool_offset = np.eye(4)
        self.tool_offset[0, 3] = 0.135
        self.inv_tool_offset = np.linalg.inv(self.tool_offset)

    def fk(self, q: ArrayLike) -> np.ndarray:
        """
        Compute forward kinematics for the tool tip (TCP).
        Returns the 4x4 SE3 matrix of the tool tip w.r.t. base.
        """
        # Get the flange pose from the base class FK
        flange_pose = super().fk(q)
        # Apply tool offset: T_base_tool = T_base_flange @ T_flange_tool
        return flange_pose @ self.tool_offset

    def ik(self, target_tool_pose: np.ndarray) -> list[np.ndarray]:
        """
        Compute inverse kinematics for a target pose of the tool tip.
        Args:
            target_tool_pose: 4x4 SE3 matrix of where you want the TOOL to be.
        """
        # 1. Calculate required flange pose from the target tool pose
        # T_base_flange = T_base_tool @ inv(T_flange_tool)
        flange_pose = target_tool_pose @ self.inv_tool_offset

        # 2. Extract the wrist center position
        # Uses the last link length dh_d[5] (0.0762m) to find the joint intersection
        wrist_center = flange_pose @ np.array([0, 0, -self.dh_d[5], 1])
        
        # 3. Solve for first 3 joints (J1, J2, J3) using the wrist position
        sols_q_03 = self._ik_flange_pos(wrist_center)

        sols = []
        for q_03 in sols_q_03:
            # Get rotation of the first 3 links
            rot_03 = super().fk(q_03)[:3, :3]
            # Solve for orientation of joints 4, 5, 6 based on the FLANGE rotation
            rot_36 = rot_03.T @ flange_pose[:3, :3]

            # Standard Euler Z-Y-Z solving logic for the wrist joints
            P = rot_36
            singularity_theta4 = 0
            if np.isclose(P[2][2], 1):
                sols.append(np.concatenate([q_03, [singularity_theta4, 0, np.arctan2(P[1][0], P[0][0]) - singularity_theta4]]))
            elif np.isclose(P[2][2], -1):
                sols.append(np.concatenate([q_03, [singularity_theta4, np.pi, np.arctan2(P[1][0], -P[0][0]) + singularity_theta4]]))
            else:
                theta5 = np.arccos(P[2][2])
                for s5 in [1, -1]:
                    sols.append(np.concatenate([q_03, [
                        np.arctan2(P[1][2] * s5, P[0][2] * s5),
                        -theta5 if s5 == 1 else theta5,
                        np.arctan2(P[2][1] * s5, -P[2][0] * s5)
                    ]]))
        return sols

# --- Test Script ---
if __name__ == "__main__":
    # Initialize with dummy values (replace with your actual config if testing on hardware)
    config = {
        "hh_irc": [0, 0, 0, 0, 0, 0],
        "lower_bound_irc": [-1000]*6,
        "upper_bound_irc": [1000]*6,
        "default_speed_irc256_per_ms": [100]*6,
        "default_acceleration_irc_per_ms": [10]*6,
        "gripper": {"tty_dev": None},
        "camera_name": "test"
    }
    
    robot = CRSRobotWithTool(tty_dev=None, **config)
    
    # Define a test joint configuration
    test_q = np.deg2rad([10, 20, -30, 0, 45, 10])
    
    # 1. Calculate tool tip pose via FK
    tcp_pose = robot.fk(test_q)
    print("Target TCP Position (X, Y, Z):", tcp_pose[:3, 3])
    
    # 2. Run IK to see if we can get the joints back
    ik_solutions = robot.ik(tcp_pose)
    
    print(f"Found {len(ik_solutions)} IK solutions.")
    for i, sol in enumerate(ik_solutions):
        # Verify by running FK on the solution
        result_pose = robot.fk(sol)
        if np.allclose(tcp_pose, result_pose, atol=1e-4):
            print(f"Solution {i} is VALID.")
        else:
            print(f"Solution {i} is INVALID.")
