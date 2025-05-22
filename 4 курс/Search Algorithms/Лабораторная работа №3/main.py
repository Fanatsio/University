import json
import heapq
import math
import time
import matplotlib.pyplot as plt
import numpy as np

def load_maze(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def a_star_search(maze_data, heuristic, allow_diagonal=False):
    width, height = maze_data['width'], maze_data['height']
    start, goal = tuple(maze_data['start']), tuple(maze_data['goal'])
    maze = maze_data['maze']
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited_nodes = 0
    
    while open_list:
        _, current = heapq.heappop(open_list)
        visited_nodes += 1
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_nodes
        
        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if allow_diagonal:
            neighbors.extend([(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)])
        
        for neighbor in neighbors:
            nx, ny = neighbor
            # Проверка границ перед доступом к maze[ny][nx]
            if 0 <= nx < width and 0 <= ny < height:
                if maze[ny][nx] == 0:  # Теперь доступ к maze[ny][nx] безопасен
                    tentative_g_score = g_score[current] + (1.414 if allow_diagonal and (x, y) != (nx, ny) else 1)
                    
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, visited_nodes

def visualize_maze(maze_data, path, allow_diagonal=False):
    maze = np.array(maze_data['maze'])
    _, ax = plt.subplots()
    
    ax.imshow(maze, cmap='binary', origin='upper')
    ax.set_xticks([])
    ax.set_yticks([])
    
    for x in range(maze_data['width']):
        for y in range(maze_data['height']):
            if (x, y) == tuple(maze_data['start']):
                ax.text(x, y, 'S', ha='center', va='center', color='green', fontsize=12, fontweight='bold')
            elif (x, y) == tuple(maze_data['goal']):
                ax.text(x, y, 'G', ha='center', va='center', color='red', fontsize=12, fontweight='bold')
    
    if path:
        for (x, y) in path:
            ax.add_patch(plt.Circle((x, y), 0.3, color='blue', alpha=0.6))
        
        # Draw lines between path nodes
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
    
    plt.show()

def compare_heuristics(file_paths):
    results = {}
    for file_path in file_paths:
        maze_data = load_maze(file_path)
        
        start_time = time.perf_counter()
        path_manhattan, visited_manhattan = a_star_search(maze_data, heuristic_manhattan)
        manhattan_time = time.perf_counter() - start_time
        visualize_maze(maze_data, path_manhattan)
        
        start_time = time.perf_counter()
        path_euclidean, visited_euclidean = a_star_search(maze_data, heuristic_euclidean, allow_diagonal=True)
        euclidean_time = time.perf_counter() - start_time
        visualize_maze(maze_data, path_euclidean, allow_diagonal=True)
        
        results[file_path] = {
            "manhattan": {"path_length": len(path_manhattan) if path_manhattan else 0, "visited_nodes": visited_manhattan, "time": manhattan_time},
            "euclidean": {"path_length": len(path_euclidean) if path_euclidean else 0, "visited_nodes": visited_euclidean, "time": euclidean_time}
        }
    
    return results

if __name__ == "__main__":
    file_paths = [
        "maze_10x10.json",
        "maze_20x20.json",
        "maze_nxm.json"
    ]
    results = compare_heuristics(file_paths)
    
    for file_path, result in results.items():
        print(f"Maze from {file_path}:")
        print(f"Manhattan Heuristic: Path Length = {result['manhattan']['path_length']}, Visited Nodes = {result['manhattan']['visited_nodes']}, Time = {result['manhattan']['time']:.6f} sec")
        print(f"Euclidean Heuristic: Path Length = {result['euclidean']['path_length']}, Visited Nodes = {result['euclidean']['visited_nodes']}, Time = {result['euclidean']['time']:.6f} sec")
