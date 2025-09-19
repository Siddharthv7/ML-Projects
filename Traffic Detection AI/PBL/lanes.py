import tkinter as tk
import random
import time

# Function to create a grid of lanes in a hash pattern
def create_grid(rows, cols):
    lanes = []
    for row in range(rows):
        lane_row = []
        for col in range(cols):
            # Randomly assign traffic to the lane (red if traffic, green if clear)
            traffic = 'T' if random.choice([True, False]) else 'N'
            lane_row.append(traffic)  # Store traffic status for each lane
        lanes.append(lane_row)
    return lanes

# Function to find the best path (A* algorithm)
def find_best_path(lanes, start, end):
    rows = len(lanes)
    cols = len(lanes[0]) if rows > 0 else 0

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = {start}
    came_from = {}
    g_score = {pos: float('inf') for pos in [(r, c) for r in range(rows) for c in range(cols)]}
    g_score[start] = 0
    f_score = {pos: float('inf') for pos in [(r, c) for r in range(rows) for c in range(cols)]}
    f_score[start] = heuristic(start, end)

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return reversed path

        open_set.remove(current)

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Up, Right, Down, Left
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                if lanes[neighbor[0]][neighbor[1]] == 'T':  # Ignore lanes with traffic
                    continue

                tentative_g_score = g_score[current] + 1  # Assume cost to neighbor is 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    open_set.add(neighbor)

    return []  # Return empty path if no route found

# Function to find a path of least resistance if the optimal path is not available
def find_least_resistance_path(lanes, start, end):
    rows = len(lanes)
    cols = len(lanes[0]) if rows > 0 else 0

    open_set = {start}
    came_from = {}
    g_score = {pos: float('inf') for pos in [(r, c) for r in range(rows) for c in range(cols)]}
    g_score[start] = 0

    while open_set:
        current = min(open_set, key=lambda pos: g_score[pos])

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return reversed path

        open_set.remove(current)

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Up, Right, Down, Left
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                # Cost of lane: 0 for clear, 1 for traffic
                cost = 1 if lanes[neighbor[0]][neighbor[1]] == 'T' else 0

                tentative_g_score = g_score[current] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    open_set.add(neighbor)

    return []  # Return empty path if no route found

# Function to draw lanes and animate the car
def draw_and_animate(lanes, path, lane_width):
    root = tk.Tk()
    root.title("Traffic Visualization with Optimal Path")
    canvas = tk.Canvas(root, width=len(lanes[0]) * lane_width, height=len(lanes) * lane_width, bg="grey")
    canvas.pack()

    # Draw lanes with their colors
    for r in range(len(lanes)):
        for c in range(len(lanes[r])):
            color = "#e8776d" if lanes[r][c] == 'T' else "#79db45"
            x1 = c * lane_width
            y1 = r * lane_width
            x2 = x1 + lane_width
            y2 = y1 + lane_width
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    # Animate the car along the path
    for (row, col) in path:
        x1 = col * lane_width + lane_width // 4
        y1 = row * lane_width + lane_width // 4
        car = canvas.create_rectangle(x1, y1, x1 + lane_width // 2, y1 + lane_width // 2, fill="blue")
        
        # Move the car along the path
        for _ in range(lane_width // 2):
            canvas.move(car, 1, 0)  # Move right
            canvas.update()
            time.sleep(0.02)

        for _ in range(lane_width // 2):
            canvas.move(car, 0, 1)  # Move down
            canvas.update()
            time.sleep(0.02)

    root.mainloop()

# Example usage
if __name__ == "__main__":
    # Set grid dimensions
    rows, cols, lane_width = 6, 6, 100
    
    # Create lanes and get their traffic status
    lanes = create_grid(rows, cols)

    # Define start and end points
    start = (0, 0)  # Top-left corner
    end = (rows - 1, cols - 1)  # Bottom-right corner

    # Find the best path avoiding traffic
    best_path = find_best_path(lanes, start, end)

    # If no optimal path found, look for the path of least resistance
    if not best_path:
        print("Optimal path not available. Searching for path of least resistance...")
        best_path = find_least_resistance_path(lanes, start, end)

    if best_path:
        print("Path found:", best_path)
        # Animate the lanes and car along the best path
        draw_and_animate(lanes, best_path, lane_width)
    else:
        print("No available path found.")
