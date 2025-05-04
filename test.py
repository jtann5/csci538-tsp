from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import ConcordeSolver


if __name__ == "__main__":
    graph = EuclideanTSPGraph()
    solver = LLMSolver("gpt-4o")
    solver2 = LLMSolver("o1")

    esolver = ConcordeSolver()

    #graph.generate_random(10)
    #graph.save_to_file("test1.tsp")
    graph.load_from_file("test1.tsp")
    print(graph)
    #print(solver.analyze(graph))
    graph.set_solution_from_string(solver.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()

    graph.set_solution(esolver.analyze(graph))
    print(graph.solution)
    print(graph.get_solution_cost())
    graph.show()
    