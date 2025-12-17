import numpy as np

class Maze:
    def __init__(self, start_x=0, start_y=0, start_z=0):
        self.points = []

        self.position = np.array([start_x, start_y, start_z], dtype=float)

        self.direction = np.array([0, 0, 1], dtype=float)  # Initially facing along the x-axis

        self.points.append(self.position.copy())

    def add_straight(self, goal, step=0.001):
        goal = np.array(goal, dtype=float)
        vec = goal - self.position
        print(vec)
        self.direction = (vec)/np.linalg.norm(vec)
        print(self.direction)
        distance = np.linalg.norm(vec)
        print(distance)

        num_steps = int(distance / step)
        print(num_steps)

        for i in range(1, num_steps + 1):
            self.position = (vec) * (i/num_steps)
            self.points.append(self.position.copy())

        self.position = goal

    def add_turn(self, axis, angle_degrees, radius, step_degrees=1):
        # 1. Always use positive steps so points are generated in order (Start -> End)
        step_rad = np.radians(abs(step_degrees))
        target_angle_rad = np.radians(abs(angle_degrees))
        sign = np.sign(angle_degrees) # +1 for Left, -1 for Right

        # 2. Define Axis
        if axis == 'x':   rot_axis = np.array([1, 0, 0], dtype=float)
        elif axis == 'y': rot_axis = np.array([0, 1, 0], dtype=float)
        elif axis == 'z': rot_axis = np.array([0, 0, 1], dtype=float)
        else: raise ValueError("Axis must be 'x', 'y', or 'z'")

        # 3. Find Center
        # Left = Cross(Axis, Direction). 
        # If sign is -1 (Right turn), Center is to the Right (-Left).
        left_vec = np.cross(rot_axis, self.direction)
        left_vec /= np.linalg.norm(left_vec)
        
        center = self.position + (left_vec * radius * sign)

        # 4. Define Basis Vectors
        # U = Radius Vector (Center -> Start)
        u = self.position - center
        
        # V = Tangent Vector. 
        # If turning Right (sign -1), we need the logic to still move "Forward".
        # The standard circle formula moves Counter-Clockwise (Left).
        # To move Clockwise (Right) while keeping theta positive, we can just inverted the logic
        # OR simpler: Use the standard formula but note that 'u' and 'center' changed.
        
        # Let's stick to the robust vector math:
        # We need a vector V that is perpendicular to U and Axis.
        # It must point in the direction of motion.
        v = self.direction * radius

        # 5. Generate Points
        num_steps = int(target_angle_rad / step_rad)
        
        for i in range(1, num_steps + 1):
            theta = step_rad * i # Always positive, so index i increases 1..N
            
            # The magic is here:
            # If we turn Left (+), we sweep angle +theta.
            # If we turn Right (-), we sweep angle -theta.
            # This ensures we move "Forward" along the curve in the correct direction.
            effective_angle = theta * sign
            
            new_pos = center + (u * np.cos(effective_angle)) + (v * np.sin(effective_angle))
            
            self.points.append(new_pos)
            self.position = new_pos

        # 6. Final Point (Exact)
        final_angle = target_angle_rad * sign
        self.position = center + (u * np.cos(final_angle)) + (v * np.sin(final_angle))
        self.points.append(self.position.copy())

        # 7. Update Direction
        # Tangent = Derivative of position
        # d/dt( u*cos(t*s) + v*sin(t*s) ) -> s * (-u*sin(t*s) + v*cos(t*s))
        # Note the 's' (sign) pulls out of the chain rule.
        new_dir = sign * (-u * np.sin(final_angle) + v * np.cos(final_angle))
        self.direction = new_dir / np.linalg.norm(new_dir)


    def get_points(self):
        return np.array(self.points)
    
    def plot(self, ax):
        points = self.get_points()
        ax.plot(points[:, 0], points[:, 1], points[:, 2], color='blue')


    