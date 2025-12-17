import maze
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


maze_A = maze.Maze()
maze_A.add_straight([0, 0, 0.2], step=0.01)


maze_B = maze.Maze()
maze_B.add_straight([0, 0, 0.08], step=0.01)
maze_B.add_turn('y', -90, 0.05, step_degrees=3)


if __name__ == "__main__":
    print("Maze A Points:")
    print(maze_A.get_points())
    print("\nMaze B Points:")
    print(maze_B.get_points())

    fig = plt.figure(figsize=(10, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    # Set equal axis limits for both subplots
    max_range = 0.2
    for ax in [ax1, ax2]:
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([0, max_range])

    maze_A.plot(ax1)
    ax1.set_title('Maze A')
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')

    maze_B.plot(ax2)
    ax2.set_title('Maze B')
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')

    plt.show()




