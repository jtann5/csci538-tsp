from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import DynamicProgrammingSolver
from heuristic import NearestNeighborSolver, GreedySolver, RandomizedSolver

if __name__ == "__main__":
    graph = EuclideanTSPGraph()

    solver = LLMSolver("gpt-4o")
    solver2 = LLMSolver("o1")

    nearest = NearestNeighborSolver(0)
    greedy = GreedySolver(0)
    randomized = RandomizedSolver(0)

    esolver = DynamicProgrammingSolver()

    #graph.generate_random(10)
    #graph.save_to_file("test1.tsp")
    graph.load_from_file("tsp10/tsp10-24.tsp")
    print(graph)
    print("\n\n")

    print("Exact:")
    graph.set_solution(esolver.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    print("\n\n")

    print("Nearest Neighbor:")
    graph.set_solution(nearest.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    print("\n\n")

    print("Randomized:")
    graph.set_solution(randomized.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    print("\n\n")

    print("Greedy:")
    graph.set_solution(greedy.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    print("\n\n")

    print("LLM:")
    graph.set_solution(solver.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    print("\n\n")