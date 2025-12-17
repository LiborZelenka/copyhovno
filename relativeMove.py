#!/usr/bin/env python
import numpy as np
from ctu_crs import CRS97

def test_relative_move():
    # 1. Initialize
    robot = CRS97()
    robot.initialize()
    
    # 2. Get the current joint configuration and calculate Forward Kinematics
    q_current = robot.get_q()
    current_pose = robot.fk(q_current)
    
    # Extract current position
    curr_x, curr_y, curr_z = current_pose[:3, 3]
    
    print("--- ROBOT STATUS ---")
    print(f"Current Joint Angles (rad): {np.round(q_current, 3)}")
    print(f"Current Cartesian Pos (m): X={curr_x:.3f}, Y={curr_y:.3f}, Z={curr_z:.3f}")
    print("--------------------")

    # 3. Define a target slightly above the current position (Z + 0.05m)
    #    We copy the ENTIRE pose matrix to keep the orientation exactly the same.
    target_pose = current_pose.copy()
    target_pose[2, 3] += 0.05  # Add 5cm to Z axis

    print(f"Attempting to move to: X={curr_x:.3f}, Y={curr_y:.3f}, Z={target_pose[2, 3]:.3f}")

    # 4. Solve IK
    ik_sols = robot.ik(target_pose)
    
    # Check 1: Did math find any solution?
    if len(ik_sols) == 0:
        print("FAILURE: Inverse Kinematics found NO mathematical solution.")
        print("The target is likely physically unreachable (too far/too high).")
        robot.close()
        return

    # Check 2: Are solutions within joint limits?
    valid_sols = [q for q in ik_sols if robot.in_limits(q)]
    
    if not valid_sols:
        print(f"FAILURE: found {len(ik_sols)} math solutions, but ALL violate joint limits.")
        print("Robot cannot reach this pose safely.")
        robot.close()
        return

    # 5. Move to the closest valid solution
    print(f"SUCCESS: Found {len(valid_sols)} valid solutions. Moving...")
    closest_sol = min(valid_sols, key=lambda q: np.linalg.norm(q - q_current))
    
    robot.move_to_q(closest_sol)
    robot.wait_for_motion_stop()
    print("Motion Complete.")
    
    robot.close()

if __name__ == "__main__":
    test_relative_move()
