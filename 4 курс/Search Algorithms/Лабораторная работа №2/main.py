import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque
import time

def generate_connected_graph(n, p, weighted=False):
    while True:
        G = nx.gnp_random_graph(n, p, directed=False)
        if nx.is_connected(G):
            break
    
    if weighted:
        for (u, v) in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 10)
    
    return G

def bfs(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])
    order = []
    
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            queue.extend(neighbor for neighbor in graph.neighbors(vertex) if neighbor not in visited)
    
    return order

def dfs(graph, start_vertex):
    visited = set()
    order = []
    
    def dfs_recursive(vertex):
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            for neighbor in graph.neighbors(vertex):
                dfs_recursive(neighbor)
    
    dfs_recursive(start_vertex)
    return order

def dijkstra(graph, start_vertex):
    return nx.single_source_dijkstra_path_length(graph, start_vertex)

def draw_graph(graph, title):
    pos = nx.kamada_kawai_layout(graph)
    plt.figure(figsize=(8, 6))
    plt.title(title)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    
    if nx.get_edge_attributes(graph, 'weight'):
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    
    plt.show()

# Генерация графов
sizes = [20, 40, 60, 80, 100]
p = 0.3  # Вероятность наличия ребра

unweighted_graphs = [(generate_connected_graph(n, p), f"Невзвешенный граф ({n} вершин)") for n in sizes]
weighted_graphs = [(generate_connected_graph(n, p, weighted=True), f"Взвешенный граф ({n} вершин)") for n in sizes]

# Словарь для хранения времени выполнения
time_results = {
    "BFS": [],
    "DFS": [],
    "Dijkstra": []
}

# Применение алгоритмов ко всем графам
for graph, title in unweighted_graphs + weighted_graphs:
    start_vertex = list(graph.nodes())[0]
    
    # BFS
    start_time = time.perf_counter()
    bfs_order = bfs(graph, start_vertex)
    bfs_time = time.perf_counter() - start_time
    time_results["BFS"].append(bfs_time)
    
    # DFS
    start_time = time.perf_counter()
    dfs_order = dfs(graph, start_vertex)
    dfs_time = time.perf_counter() - start_time
    time_results["DFS"].append(dfs_time)
    
    # Dijkstra (только для взвешенных графов)
    if "Взвешенный" in title:
        start_time = time.perf_counter()
        dijkstra_distances = dijkstra(graph, start_vertex)
        dijkstra_time = time.perf_counter() - start_time
        time_results["Dijkstra"].append(dijkstra_time)
    else:
        time_results["Dijkstra"].append(None)  # Для невзвешенных графов Dijkstra не применяется
    
    print(f"{title}:")
    print(f"  BFS порядок: {bfs_order}")
    print(f"  Время BFS: {bfs_time:.6f} сек")
    print(f"  DFS порядок: {dfs_order}")
    print(f"  Время DFS: {dfs_time:.6f} сек")
    if "Взвешенный" in title:
        print(f"  Dijkstra расстояния: {dijkstra_distances}")
        print(f"  Время Dijkstra: {dijkstra_time:.6f} сек")
    print()

# Визуализация графов (опционально)
# for graph, title in unweighted_graphs + weighted_graphs:
#     draw_graph(graph, title)

# Построение графика сравнения времени выполнения
plt.figure(figsize=(10, 6))

# Данные для взвешенных графов
bfs_times_weighted = time_results["BFS"][len(sizes):]  # Взвешенные графы
dfs_times_weighted = time_results["DFS"][len(sizes):]  # Взвешенные графы
dijkstra_times_weighted = [t for t in time_results["Dijkstra"][len(sizes):] if t is not None]  # Взвешенные графы

plt.plot(sizes, bfs_times_weighted, marker='o', label="BFS (взвешенные)", color='blue')
plt.plot(sizes, dfs_times_weighted, marker='o', label="DFS (взвешенные)", color='red')
plt.plot(sizes, dijkstra_times_weighted, marker='o', label="Dijkstra (взвешенные)", color='green')

plt.xlabel("Количество вершин")
plt.ylabel("Время выполнения (сек)")
plt.title("Сравнение времени выполнения алгоритмов (взвешенные графы)")
plt.legend()
plt.grid(True)
plt.show()