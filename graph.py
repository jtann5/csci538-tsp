import random
import math
import matplotlib.pyplot as plt

class EuclideanTSPGraph:
    def __init__(self, name="tsp graph"):
        self.name = name
        self.nodes = {}  # node_id: (x, y)
        self.dimension = 0
        self.edge_weight_type = "EUC_2D"
        self.solution = []
        self.solution_cost = None

    def add_node(self, node_id, x, y):
        # Check if the coordinate already exists
        for node in self.nodes.values():
            if node == (x, y):
                raise ValueError(f"Node with coordinates ({x}, {y}) already exists.")
        self.nodes[node_id] = (x, y)
        self.dimension = len(self.nodes)

    def generate_random(self, num_nodes, x_range=(0, 100), y_range=(0, 100)):
        self.nodes = {}
        attempts = 0
        while len(self.nodes) < num_nodes and attempts < 1000:
            node_id = len(self.nodes)
            x = random.randint(*x_range)
            y = random.randint(*y_range)
            try:
                self.add_node(node_id, x, y)
            except ValueError:  # Skip duplicate nodes
                attempts += 1
                continue
        if len(self.nodes) != num_nodes:
            raise ValueError("Failed to generate a complete set of unique nodes after 1000 attempts.")

    def distance(self, node1, node2):
        x1, y1 = self.nodes[node1]
        x2, y2 = self.nodes[node2]
        return int(round(math.hypot(x1 - x2, y1 - y2)))

    def to_tsp_format(self):
        lines = [
            f"NAME: {self.name}",
            "TYPE: TSP",
            f"DIMENSION: {self.dimension}",
            f"EDGE_WEIGHT_TYPE: {self.edge_weight_type}",
            "NODE_COORD_SECTION"
        ]
        for node_id in sorted(self.nodes):
            x, y = self.nodes[node_id]
            lines.append(f"{node_id} {x:.0f} {y:.0f}")
        lines.append("EOF")
        return "\n".join(lines)

    def save_to_file(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.to_tsp_format())

    def load_from_file(self, filepath, check_dimension=True):
        with open(filepath, 'r') as f:
            graph_data = f.read().splitlines()

        node_section_started = False
        expected_dimension = None
        node_lines = []

        for line in graph_data:
            line = line.strip()
            if not line or line.startswith("COMMENT"):
                continue

            if line.startswith("NAME"):
                self.name = line.split(":", 1)[1].strip()
            elif line.startswith("TYPE"):
                type_val = line.split(":", 1)[1].strip()
                if type_val.upper() != "TSP":
                    raise ValueError(f"Invalid TYPE: expected TSP, got {type_val}")
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                weight_type = line.split(":", 1)[1].strip()
                if weight_type.upper() != "EUC_2D":
                    raise ValueError(f"Unsupported EDGE_WEIGHT_TYPE: expected EUC_2D, got {weight_type}")
            elif line.startswith("DIMENSION"):
                expected_dimension = int(line.split(":", 1)[1].strip())
            elif line.startswith("NODE_COORD_SECTION"):
                node_section_started = True
            elif node_section_started:
                if line.upper().startswith("EOF"):
                    break
                node_lines.append(line)

        self.nodes = {}
        for line in node_lines:
            parts = list(map(float, line.strip().split()))
            if len(parts) != 3:
                raise ValueError(f"Invalid node format: {line}")
            self.add_node(int(parts[0]), parts[1], parts[2])

        if check_dimension and expected_dimension is not None:
            if len(self.nodes) != expected_dimension:
                raise ValueError(f"Node count {len(self.nodes)} does not match DIMENSION {expected_dimension}")


    def set_solution(self, route):
        if isinstance(route, str) and route.strip():
            self.set_solution_from_string(route)
            return
        
        if set(route) != set(self.nodes.keys()):
            raise ValueError("Solution does not contain all nodes.")
        self.solution = route
        self.solution_cost = self.get_solution_cost() if self.is_valid_solution() else None

    def set_solution_from_string(self, solution_str):
        try:
            # Remove brackets and whitespace, split by comma, convert to int
            cleaned = solution_str.strip().strip("[]")
            route = [int(x.strip()) for x in cleaned.split(",")]
            self.set_solution(route)
            return True
        except Exception as e:
            print(f"Failed to set solution: {e}")
            return False

    def is_valid_solution(self):
        if len(self.solution) != self.dimension:
            return False
        for i in range(len(self.solution)):
            a = self.solution[i]
            b = self.solution[(i + 1) % len(self.solution)]  # Return to start
            if (a, b) not in self.edges() and (b, a) not in self.edges():
                return False
        return True

    def get_solution_cost(self):
        if not self.is_valid_solution():
            raise ValueError("Invalid solution. Cannot compute cost.")
        total = 0
        for i in range(len(self.solution)):
            a = self.solution[i]
            b = self.solution[(i + 1) % len(self.solution)]
            total += self.distance(a, b)
        return total

    def edges(self):
        """Generate the edges (pairs of nodes) for this graph."""
        edges = {}
        for a in self.nodes:
            for b in self.nodes:
                if a != b:
                    edges[(a, b)] = self.distance(a, b)
        return edges
    
    def to_distance_matrix(self):
        """Converts the graph to a distance matrix."""
        matrix = []
        nodes_list = list(self.nodes.keys())
        for i in nodes_list:
            row = []
            for j in nodes_list:
                if i == j:
                    row.append(0)
                else:
                    row.append(self.distance(i, j))
            matrix.append(row)
        return matrix
    
    def show(self, show_solution=True, show_all_edges=True):
        plt.figure(figsize=(8, 6))
        x = [coord[0] for coord in self.nodes.values()]
        y = [coord[1] for coord in self.nodes.values()]
        
        # Draw nodes
        for node_id, (xi, yi) in self.nodes.items():
            plt.plot(xi, yi, 'bo')
            plt.text(xi + 1, yi + 1, str(node_id), fontsize=12)

        # Draw solution path if available
        if show_solution and self.solution:
            path = self.solution + [self.solution[0]]  # Return to start
            for i in range(len(self.solution)):
                a = self.nodes[path[i]]
                b = self.nodes[path[i + 1]]
                plt.plot([a[0], b[0]], [a[1], b[1]], 'r-')

        # Draw all edges (complete graph) if requested
        if show_all_edges:
            for i, (id1, (x1, y1)) in enumerate(self.nodes.items()):
                for j, (id2, (x2, y2)) in enumerate(self.nodes.items()):
                    if id1 != id2 and id1 < id2:  # Avoid duplicate lines
                        plt.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=0.5)

        plt.title(f"TSP Graph - {self.name}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.axis("equal")
        plt.show()

    def __str__(self):
        return self.to_tsp_format()

# Example usage
if __name__ == "__main__":
    graph = EuclideanTSPGraph()
    graph.add_node(1, 10, 20)
    graph.add_node(2, 30, 40)
    graph.add_node(3, 50, 10)
    graph.add_node(4, 60, 60)
    graph.add_node(5, 70, 20)
    print(graph)

    # Example of loading a TSP file
    # graph.load_from_file('example.tsp')
    # print(graph)

    # Example of setting and validating a solution
    graph.set_solution([1, 2, 3, 4, 5])
    print("Solution is valid:", graph.is_valid_solution())
    print("Solution cost:", graph.get_solution_cost())
