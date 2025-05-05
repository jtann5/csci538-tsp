from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np

class DynamicProgrammingSolver:
    def __init__(self):
        pass

    def analyze(self, graph):
        # Convert the graph's nodes and distances into a distance matrix
        distance_matrix = np.array(graph.to_distance_matrix())
        
        # Solve the TSP using the Concorde solver through pytsp
        solution, cost = solve_tsp_dynamic_programming(distance_matrix)
        
        # Return the solution path and cost
        return solution
