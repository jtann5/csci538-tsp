import random
import json

class TSPGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = {} # Dict of (node1, node2): weight
        self.solution = [] # List of node names representing the route

    def add_edge(self, node1, node2, weight):
        self.nodes.update([node1, node2])
        self.edges[(node1, node2)] = weight
        self.edges[(node2, node1)] = weight  # Undirected graph

    def try_generate_graph(self, num_nodes, edge_probability=0.5, max_weight=100, max_tries=100):
        for _ in range(max_tries):
            self.generate_random(num_nodes, edge_probability, max_weight)
            
            if self.is_valid_graph():
                return True 
            
        return False

    def generate_random(self, num_nodes, edge_probability=0.5, max_weight=100):
        self.nodes = {i for i in range(num_nodes)}  # Nodes as strings for clarity
        self.edges = {}
        
        # Generate edges based on edge_probability
        for a in self.nodes:
            for b in self.nodes:
                if a != b and (a, b) not in self.edges:
                    if random.random() < edge_probability:
                        weight = random.randint(1, max_weight)
                        self.add_edge(a, b, weight)

    def load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            graph_data = json.load(f)
            
        self.nodes = set(graph_data["nodes"])  # Numbers as nodes
        self.edges = {}
        
        for edge in graph_data["edges"]:
            self.edges[(edge["from"], edge["to"])] = edge["weight"]
            self.edges[(edge["to"], edge["from"])] = edge["weight"]  # Ensuring symmetry
        
        print(f"Graph loaded from {filepath}")

    def save_to_file(self, filepath):
        graph_data = {
            "nodes": list(self.nodes),  # Nodes as numbers
            "edges": [{"from": a, "to": b, "weight": weight} for (a, b), weight in self.edges.items()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"Graph saved to {filepath}")

    def is_valid_graph(self):
        # Check 1: The graph must contain at least two nodes
        if len(self.nodes) < 2:
            return False

        # Check 2: Every edge must connect valid nodes
        for (a, b) in self.edges:
            if a not in self.nodes or b not in self.nodes:
                return False

        # Check 3: No self-loops (edges from a node to itself)
        for (a, b) in self.edges:
            if a == b:
                return False

        # Check 4: Ensure all edges have valid (positive) weights
        for (a, b), weight in self.edges.items():
            if weight <= 0:
                return False
        
        # (Optional) Check 5: Ensure the graph is connected (only for undirected graphs)
        # This can be checked via a Depth-First Search (DFS) or Breadth-First Search (BFS).
        # For this, you would need to traverse all nodes and see if they are all reachable.
        if not self.is_connected():
            return False
        
        return True
    
    def is_connected(self):
        # Simple DFS or BFS to check if the graph is connected.
        visited = set()
        
        # Start DFS from any node (we choose the first node in the set)
        def dfs(node):
            visited.add(node)
            for (a, b) in self.edges:
                if a == node and b not in visited:
                    dfs(b)
                elif b == node and a not in visited:
                    dfs(a)
        
        # Start DFS from an arbitrary node
        dfs(next(iter(self.nodes)))
        
        # If we've visited all nodes, the graph is connected
        return visited == self.nodes

    def set_solution(self, route):
        self.solution = route
        self.solution_cost = self.get_solution_cost() if self.is_valid_solution() else None

    def is_valid_solution(self):
        if set(self.solution) != self.nodes:
            return False
        if len(self.solution) != len(self.nodes):
            return False
        for i in range(len(self.solution)):
            a = self.solution[i]
            b = self.solution[(i + 1) % len(self.solution)]  # Return to start
            if (a, b) not in self.edges:
                return False
        return True

    def get_solution_cost(self):
        if not self.is_valid_solution():
            raise ValueError("Invalid solution. Cannot compute cost.")
        total = 0
        for i in range(len(self.solution)):
            a = self.solution[i]
            b = self.solution[(i + 1) % len(self.solution)]
            total += self.edges[(a, b)]
        return total
    
    def to_json_prompt(self):
        edges_list = []
        seen = set()
        for (a, b), weight in self.edges.items():
            if (b, a) not in seen:
                edges_list.append({"from": a, "to": b, "weight": weight})
                seen.add((a, b))

        return {
            "nodes": sorted(self.nodes),
            "edges": edges_list
        }
    
    def __str__(self):
        output = "Graph for Traveling Salesman Problem\n"
        output += f"Nodes: {sorted(self.nodes)}\n"
        output += "Edges:\n"
        
        seen = set()
        for (a, b), weight in sorted(self.edges.items()):
            if (b, a) not in seen:  # Avoid printing duplicate undirected edges
                output += f"  {a} <-> {b} with weight {weight}\n"
                seen.add((a, b))
        
        return output