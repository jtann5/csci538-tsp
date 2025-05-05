import os
import re
import csv
import time

from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import DynamicProgrammingSolver
from heuristic import NearestNeighborSolver, GreedySolver

def variance(llm_solver: LLMSolver, data, filepath):
    return

def load_optimal_costs(csv_path):
    optimal_map = {}  # filename (without .tsp) -> cost
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = row['filename'].removesuffix(".tsp")
            cost = float(row['cost'])  # assumes 'cost' column exists
            optimal_map[filename] = cost
    return optimal_map


def collect_data(solver, data_directory_or_files, output_path, exact_values=None):
    if isinstance(data_directory_or_files, list):
        files = data_directory_or_files
    else:
        files = [f for f in os.listdir(data_directory_or_files) if f.endswith(".tsp")]

        def extract_numeric_parts(filename):
            return [int(part) for part in re.findall(r'\d+', filename)]

        files = sorted(files, key=extract_numeric_parts)

    if exact_values:
        optimal_cost_map = load_optimal_costs(exact_values)
    else:
        esolver = DynamicProgrammingSolver()
    #solver = solver_class()

    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "cost", "time (s)", "optimality gap (%)"])
        
        total_cost = 0
        total_time = 0
        total_gap = 0
        num_files = 0

        for filename in files:
            file_path = os.path.join(data_directory_or_files, filename) if not isinstance(data_directory_or_files, list) else filename
            
            graph = EuclideanTSPGraph()
            graph.load_from_file(file_path)

            start_time = time.time()
            graph.set_solution(solver.analyze(graph))
            end_time = time.time()
            # for real time use time.time()
            # for cpu time use time.process_time()

            elapsed_time = end_time - start_time

            cost = graph.get_solution_cost()

            if exact_values:
                optimal_cost = optimal_cost_map.get(filename.removesuffix(".tsp"))
                if optimal_cost is None:
                    raise ValueError(f"No optimal cost found for {filename}")
            else:
                if  isinstance(solver, DynamicProgrammingSolver):
                    optimal_cost = cost
                else:
                    graph.set_solution(esolver.analyze(graph))
                    optimal_cost = graph.get_solution_cost()

            optimality_gap = (cost - optimal_cost) / optimal_cost * 100
            
            # Write the row for this file
            writer.writerow([os.path.basename(filename).removesuffix(".tsp"), cost, f"{elapsed_time:.5f}", optimality_gap])

            total_cost += cost
            total_time += elapsed_time
            total_gap += optimality_gap if optimality_gap is not None else 0
            num_files += 1

            print("Evluated: " + str([os.path.basename(filename).removesuffix(".tsp"), cost, f"{elapsed_time:.5f}", optimality_gap]))

        mean_cost = total_cost / num_files
        mean_time = total_time / num_files
        mean_gap = total_gap / num_files if num_files > 0 else 0
        
        # Write the mean values at the end
        writer.writerow(["Mean", mean_cost, f"{mean_time:.5f}", mean_gap])





if __name__ == "__main__":
    for i in [20, 30]:
        solver = DynamicProgrammingSolver()
        collect_data(solver, "tsp"+str(i), "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # solver = NearestNeighborSolver(0)
        # collect_data(solver, "tsp"+str(i), "results/tsp"+str(i)+"/NearestNeighborSolver-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # solver = GreedySolver(0)
        # collect_data(solver, "tsp"+str(i), "results/tsp"+str(i)+"/GreedySolver-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # solver = LLMSolver("gpt-4o")
        # collect_data(solver, "tsp"+str(i), "results/tsp"+str(i)+"/LLMSolver-gpt-4o-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # solver = LLMSolver("o1")
        # collect_data(solver, "tsp"+str(i), "results/tsp"+str(i)+"/LLMSolver-o1-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")
