#!/usr/bin/env python
#
# Helper script to move CRS97 to a Cartesian position (x, y, z)
# preserving current orientation.
#

import numpy as np
from ctu_crs import CRS97

def move_to_pos(robot: CRS97, x: float, y: float, z: float):
    """
    Moves the robot to the specified Cartesian coordinates (x, y, z)
    while maintaining the current end-effector orientation.
    """
    # 1. Get current configuration and pose
    q_current = robot.get_q()
    current_pose = robot.fk(q_current)

    # 2. Create target pose: copy current rotation, update translation to target x,y,z
    target_pose = current_pose.copy()
    target_pose[:3, 3] = [x, y, z]

    print(f"Planning move to: x={x:.3f}, y={y:.3f}, z={z:.3f}")

    # 3. Solve Inverse Kinematics
    ik_sols = robot.ik(target_pose)

    # 4. Filter for solutions that are within joint limits
    valid_sols = [sol for sol in ik_sols if robot.in_limits(sol)]

    if not valid_sols:
        print("Error: No valid IK solutions found (unreachable or out of limits).")
        return

    # 5. Find the solution closest to the current joint configuration
    #    to minimize unnecessary rotation.
    closest_solution = min(valid_sols, key=lambda q: np.linalg.norm(q - q_current))

    # 6. Execute movement
    robot.move_to_q(closest_solution)
    robot.wait_for_motion_stop()
    print("Movement finished.")


if __name__ == "__main__":
    # Initialize the robot
    robot = CRS97()
    robot.initialize()

    try:
        # Example 1: Move to a specific point (Example coordinates)
        # Note: Ensure these coordinates are reachable for your specific setup!
        # This keeps the orientation the robot has after homing/initialization.
        move_to_pos(robot, 0.25, 0.0, 0.25)
        
        # Example 2: Move 10cm up from the current position
        q_curr = robot.get_q()
        curr_pos = robot.fk(q_curr)[:3, 3]
        move_to_pos(robot, curr_pos[0], curr_pos[1], curr_pos[2] + 0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always close the connection
        robot.close()
