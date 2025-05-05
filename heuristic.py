import random

class NearestNeighborSolver:
    def __init__(self, start_node=None):
        self.start_node = start_node

    def analyze(self, graph):
        if self.start_node is None:
            current = random.choice(list(graph.nodes.keys()))
        else:
            current = self.start_node

        unvisited = set(graph.nodes.keys())
        tour = [current]
        unvisited.remove(current)

        while unvisited:
            next_node = min(unvisited, key=lambda node: graph.distance(current, node))
            tour.append(next_node)
            unvisited.remove(next_node)
            current = next_node

        #graph.set_solution(tour)
        return tour

class GreedySolver:
    def __init__(self, start_node=None):
        self.start_node = start_node

    def analyze(self, graph):
        edges = sorted(graph.edges().items(), key=lambda item: item[1])
        parent = {node: node for node in graph.nodes}

        def find(n):
            while parent[n] != n:
                parent[n] = parent[parent[n]]
                n = parent[n]
            return n

        def union(n1, n2):
            root1, root2 = find(n1), find(n2)
            parent[root1] = root2

        used_edges = []
        degrees = {node: 0 for node in graph.nodes}

        for (u, v), dist in edges:
            if degrees[u] >= 2 or degrees[v] >= 2:
                continue
            if find(u) != find(v) or len(used_edges) == graph.dimension - 1:
                used_edges.append((u, v))
                union(u, v)
                degrees[u] += 1
                degrees[v] += 1
            if len(used_edges) == graph.dimension:
                break

        from collections import defaultdict

        adj = defaultdict(list)
        for u, v in used_edges:
            adj[u].append(v)
            adj[v].append(u)

        # Choose start node
        if self.start_node is not None:
            if self.start_node not in graph.nodes:
                raise ValueError(f"Start node {self.start_node} not in graph.")
            start = self.start_node
        else:
            start = used_edges[0][0]  # default to first edge's node

        # Reconstruct the tour
        tour = []
        visited = set()

        def dfs(u):
            visited.add(u)
            tour.append(u)
            for v in adj[u]:
                if v not in visited:
                    dfs(v)

        dfs(start)

        #graph.set_solution(tour)
        return tour
