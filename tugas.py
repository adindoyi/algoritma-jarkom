from collections import defaultdict, deque

class Graph:
    def __init__(self, edges, N):
        self.adjList = defaultdict(list)
        for (src, dest, weight) in edges:
            self.adjList[src].append((dest, weight))

def bfs(graph, source, N):
    distance = [float('inf')] * N
    distance[source] = 0
    parent = [-1] * N

    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, w in graph.adjList[u]:
            if distance[v] > distance[u] + w:
                distance[v] = distance[u] + w
                parent[v] = u  # Update parent of v
                queue.append(v)
    return distance, parent

def bellman_ford(graph, source, N):
    distance = [float('inf')] * N
    distance[source] = 0
    parent = [-1] * N

    for _ in range(N - 1):
        for u in range(N):
            for v, w in graph.adjList[u]:
                if distance[u] != float('inf') and distance[v] > distance[u] + w:
                    distance[v] = distance[u] + w
                    parent[v] = u  # Update parent of v

    return distance, parent

def topological_sort_util(graph, v, visited, stack):
    visited[v] = True
    for u, w in graph.adjList[v]:
        if not visited[u]:
            topological_sort_util(graph, u, visited, stack)
    stack.append(v)

def dag_shortest_path(graph, source, N):
    stack = []
    visited = [False] * N

    for i in range(N):
        if not visited[i]:
            topological_sort_util(graph, i, visited, stack)

    distance = [float('inf')] * N
    distance[source] = 0
    parent = [-1] * N

    while stack:
        u = stack.pop()
        if distance[u] != float('inf'):
            for v, w in graph.adjList[u]:
                if distance[v] > distance[u] + w:
                    distance[v] = distance[u] + w
                    parent[v] = u  # Update parent of v

    return distance, parent

if __name__ == "__main__":
    edges = [
        (0, 6, 2), (1, 2, -4), (1, 4, 1), (1, 6, 8), (3, 0, 3), (3, 4, 5),
        (5, 1, 2), (7, 0, 6), (7, 1, -1), (7, 3, 4), (7, 5, -4)
    ]
    n = 8
    graph = Graph(edges, n)
    source = 7

    # BFS Shortest Path
    bfs_distance, bfs_parent = bfs(graph, source, n)
    print("\nBFS shortest path parents:", bfs_parent)
    print("Breadth First Search (BFS) Shortest Path:")
    for i in range(n):
        if bfs_distance[i] != float('inf'):
            path = [i]
            parent = bfs_parent[i]
            while parent != -1:
                path.append(parent)
                parent = bfs_parent[parent]
            path_str = ' -> '.join(map(str, path[::-1]))
            print(f"dist({source}, {i}) = {bfs_distance[i]} ({path_str})")

    # Bellman-Ford Shortest Path
    bellman_distance, bellman_parent = bellman_ford(graph, source, n)
    print("\nBellman-Ford shortest path parents:", bellman_parent)
    print("Bellman-Ford Shortest Path:")
    for i in range(n):
        if bellman_distance[i] != float('inf'):
            path = [i]
            parent = bellman_parent[i]
            while parent != -1:
                path.append(parent)
                parent = bellman_parent[parent]
            path_str = ' -> '.join(map(str, path[::-1]))
            print(f"dist({source}, {i}) = {bellman_distance[i]} ({path_str})")

    # DAG Shortest Path
    dag_distance, dag_parent = dag_shortest_path(graph, source, n)
    print("\nDAG shortest path parents:", dag_parent)
    print("Directed Acyclic Graph (DAG) Shortest Path:")
    for i in range(n):
        if dag_distance[i] != float('inf'):
            path = [i]
            parent = dag_parent[i]
            while parent != -1:
                path.append(parent)
                parent = dag_parent[parent]
            path_str = ' -> '.join(map(str, path[::-1]))
            print(f"dist({source}, {i}) = {dag_distance[i]} ({path_str})")