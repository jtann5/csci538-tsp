from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import DynamicProgrammingSolver
from heuristic import NearestNeighborSolver, GreedySolver

if __name__ == "__main__":
    graph = EuclideanTSPGraph()

    solver = LLMSolver("gpt-4o")
    solver2 = LLMSolver("o1")

    nearest = NearestNeighborSolver(0)
    gready = GreedySolver(0)

    esolver = DynamicProgrammingSolver()

    graph.generate_random(10)
    graph.save_to_file("test1.tsp")
    #graph.load_from_file("tsp10/tsp10-1.tsp")
    print(graph)
    print("\n\n")

    # print("LLM:")
    # graph.set_solution_from_string(solver.analyze(graph))
    # print(graph.solution)
    # print(graph.get_solution_cost())
    # graph.show()
    # print("\n\n")

    # print("Nearest Neighbor:")
    # graph.set_solution(nearest.analyze(graph))
    # print(graph.solution)
    # print(graph.get_solution_cost())
    # graph.show()
    # print("\n\n")

    # print("Greedy:")
    # graph.set_solution(gready.analyze(graph))
    # print(graph.solution)
    # print(graph.get_solution_cost())
    # graph.show()
    # print("\n\n")

    # print("Exact:")
    # graph.set_solution(esolver.analyze(graph))
    # print(graph.solution)
    # print(graph.get_solution_cost())
    # graph.show()
    # print("\n\n")
    