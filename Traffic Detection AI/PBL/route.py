import heapq

# Function to find the best route avoiding traffic
def find_best_route(graph, start, end):
    # Priority queue to hold (cost, current_node)
    queue = [(0, start)]
    # Dictionary to hold the shortest paths
    shortest_paths = {start: (None, 0)}  # node: (previous_node, cost)

    while queue:
        (cost, current_node) = heapq.heappop(queue)

        # Stop if we reach the end node
        if current_node == end:
            break

        for neighbor, traffic_cost in graph[current_node].items():
            # Calculate the new cost
            new_cost = cost + traffic_cost
            if neighbor not in shortest_paths or new_cost < shortest_paths[neighbor][1]:
                shortest_paths[neighbor] = (current_node, new_cost)
                heapq.heappush(queue, (new_cost, neighbor))

    # Reconstruct the best route
    route = []
    while end is not None:
        route.append(end)
        end = shortest_paths[end][0]
    route.reverse()

    return route, shortest_paths[route[-1]][1]  # Return the best route and the total cost

# Example usage
if __name__ == "__main__":
    # Define the graph (roads and traffic costs)
    graph = {
        'A': {'B': 2, 'C': 1},        # A connects to B and C with costs
        'B': {'A': 2, 'D': 5, 'E': 1},
        'C': {'A': 1, 'D': 3},
        'D': {'B': 5, 'C': 3, 'E': 2},
        'E': {'B': 1, 'D': 2}
    }

    start = 'A'  # Starting intersection
    end = 'E'    # Destination intersection

    best_route, total_cost = find_best_route(graph, start, end)

    print("Best Route:", " -> ".join(best_route))
    print("Total Traffic Cost:", total_cost)
