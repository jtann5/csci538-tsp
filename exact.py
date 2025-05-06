from python_tsp.exact import solve_tsp_dynamic_programming, solve_tsp_branch_and_bound
import numpy as np

class DynamicProgrammingSolver:
    def __init__(self):
        pass

    def analyze(self, graph):
        distance_matrix = np.array(graph.to_distance_matrix())
        
        solution, cost = solve_tsp_dynamic_programming(distance_matrix)
        
        return solution
    
class BranchAndBoundSolver:
    def __init__(self):
        pass

    def analyze(self, graph):
        distance_matrix = np.array(graph.to_distance_matrix())

        solution, cost = solve_tsp_branch_and_bound(distance_matrix)

        return solution