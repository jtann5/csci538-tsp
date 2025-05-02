from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import ConcordeSolver


if __name__ == "__main__":
    graph = EuclideanTSPGraph()
    solver = LLMSolver("gpt-4o")
    solver2 = LLMSolver("o1")

    esolver = ConcordeSolver()

    graph.generate_random(20)
    graph.save_to_file("test1.tsp")
    print(graph)
    graph.set_solution(esolver.analyze(graph))
    print(graph.solution)
    graph.show()
    