import pygame
from settings import *
from boundary import *




def obstacle_w():
    walls = []
    # point = [[0, 0, width, 0], [width, 0, width, height],
    #          [width, height, 0, height], [0, height, 0, 0],
    #          [100, 100, 300, 50], [100, 100, 200, 250],
    #          [300, 50, 200, 250], [400, 100, 550, 50],
    #          [400, 100, 500, 300], [550, 50, 500, 300],
    #          [50, 450, 250, 300], [50, 450, 150, 550],
    #          [250, 300, 250, 500], [150, 550, 250, 500],
    #          [450, 350, 350, 300], [350, 300, 350, 450],
    #          [450, 350, 550, 550], [350, 450, 550, 550],
    #          [50, 250, 100, 250], [50, 250, 50, 350],
    #          [100, 250, 50, 350], [300, 200, 350, 200],
    #          [300, 200, 300, 250], [350, 200, 350, 250],
    #          [300, 250, 350, 250]]
#     point = [
#     [0, 0, width, 0],
#     [width, 0, width, height],
#     [width, height, 0, height],
#     [0, height, 0, 0],
#     # Rectangle (left-bottom corner at (50, 50), width: 200, height: 100)
#     [50, 50, 250, 50],      # Top edge
#     [250, 50, 250, 150],    # Right edge
#     [250, 150, 50, 150],    # Bottom edge
#     [50, 150, 50, 50],      # Left edge

#     # Square (left-bottom corner at (300, 50), width: 100)
#     [300, 50, 400, 50],     # Top edge
#     [400, 50, 400, 150],    # Right edge
#     [400, 150, 300, 150],   # Bottom edge
#     [300, 150, 300, 50],    # Left edge

#     # Triangle (vertices)
#     [100, 200, 150, 300],   # Left edge
#     [150, 300, 200, 200],    # Right edge
#     [200, 200, 100, 200],     # Base edge (line across)
    
#     # Circle approximation (approximated with 12 edges)
#     # Center (450, 300), radius = 50
#     [450, 300, 500, 300],   # Right
#     [500, 300, 525, 350],   # Bottom right
#     [525, 350, 500, 400],   # Bottom
#     [500, 400, 450, 400],   # Bottom left
#     [450, 400, 425, 350],   # Top left
#     [425, 350, 450, 300], # Additional obstacle

#    # Additional Rectangle (left-bottom corner at (100, 400), width: 150, height: 75)
#     [100, 400, 250, 400],   # Top edge
#     [250, 400, 250, 475],   # Right edge
#     [250, 475, 100, 475],   # Bottom edge
#     [100, 475, 100, 400],   # Left edge
#     ]


    point = [
        # Maze walls
        [0, 0, 600, 0],         # Top boundary
        [600, 0, 600, 600],     # Right boundary
        [600, 600, 0, 600],     # Bottom boundary
        [0, 600, 0, 0],         # Left boundary

        # Horizontal and vertical walls to create a maze
        [0, 100, 100, 100],     # Top left horizontal
        [100, 0, 100, 200],     # Left vertical
        [200, 100, 300, 100],   # Top middle horizontal
        [300, 0, 300, 300],     # Middle left vertical
        [400, 100, 500, 100],   # Top right horizontal
        [500, 0, 500, 200],     # Right vertical
        [200, 200, 200, 400],    # Middle vertical
        [300, 300, 400, 300],   # Middle right horizontal
        [400, 200, 400, 400],   # Right vertical
        [100, 200, 100, 300],   # Middle left vertical
        [100, 300, 200, 300],   # Middle middle horizontal
        [0, 400, 200, 400],     # Lower left horizontal
        [200, 400, 200, 500],   # Lower middle vertical
        [300, 400, 400, 400],   # Lower right horizontal
        [400, 500, 500, 500],   # Lower right horizontal
        [500, 300, 500, 500],   # Right vertical
        [100, 500, 200, 500],   # Lower left vertical
    ]

    for sublist in point:
        for i in range(0, len(sublist), 2):
            x1, y1, x2, y2 = sublist[i], sublist[i+1], sublist[(
                i+2) % len(sublist)], sublist[(i+3) % len(sublist)]
            walls.append(Boundary(x1, y1, x2, y2))
    return walls
