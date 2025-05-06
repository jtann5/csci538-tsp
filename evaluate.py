import os
import re
import csv
import time
import numpy as np

from graph import EuclideanTSPGraph
from llm_solver import LLMSolver
from exact import DynamicProgrammingSolver
from heuristic import NearestNeighborSolver, GreedySolver, RandomizedSolver

def variance(llm_solver: LLMSolver, filepath, output_path, num_tests):
    graph = EuclideanTSPGraph()
    graph.load_from_file(filepath)

    esolver = DynamicProgrammingSolver()
    graph.set_solution(esolver.analyze(graph))
    optimal_cost = graph.get_solution_cost()

    results = []

    for i in range(num_tests):
        graph.load_from_file(filepath)  # Reload to reset any prior solution

        start_time = time.time()
        route = llm_solver.analyze(graph)
        end_time = time.time()

        if isinstance(route, tuple):
            route = route[0]  # Handle (tour, cost) return style

        graph.set_solution(route)
        cost = graph.get_solution_cost()
        duration = round(end_time - start_time, 5)
        gap = round(((cost - optimal_cost) / optimal_cost) * 100, 5)

        results.append([i + 1, round(cost, 5), duration, gap])
        print("Completed trial " + str(i+1) + " on " + os.path.basename(filepath).removesuffix(".tsp"))

    # Compute stats
    np_results = np.array(results)[:, 1:].astype(float)  # skip trial index
    mean = np.mean(np_results, axis=0)
    var = np.var(np_results, axis=0, ddof=1)  # sample variance
    max_ = np.max(np_results, axis=0)
    min_ = np.min(np_results, axis=0)
    range_ = max_ - min_

    # Write results
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["trial", "cost", "time (s)", "optimality gap (%)"])
        writer.writerows(results)
        writer.writerow(["mean"] + list(np.round(mean, 5)))
        writer.writerow(["variance"] + list(np.round(var, 5)))
        writer.writerow(["max"] + list(np.round(max_, 5)))
        writer.writerow(["min"] + list(np.round(min_, 5)))
        writer.writerow(["range"] + list(np.round(range_, 5)))


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

            print("Evaluated: " + str([os.path.basename(filename).removesuffix(".tsp"), cost, f"{elapsed_time:.5f}", optimality_gap]))

        mean_cost = total_cost / num_files
        mean_time = total_time / num_files
        mean_gap = total_gap / num_files if num_files > 0 else 0
        
        # Write the mean values at the end
        writer.writerow(["Mean", mean_cost, f"{mean_time:.5f}", mean_gap])


def collect_data_no_opt(solver, data_directory_or_files, output_path):
    if isinstance(data_directory_or_files, list):
        files = data_directory_or_files
    else:
        files = [f for f in os.listdir(data_directory_or_files) if f.endswith(".tsp")]

        def extract_numeric_parts(filename):
            return [int(part) for part in re.findall(r'\d+', filename)]

        files = sorted(files, key=extract_numeric_parts)


    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "cost", "time (s)", "optimality gap (%)"])
        
        total_cost = 0
        total_time = 0
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

            
            # Write the row for this file
            writer.writerow([os.path.basename(filename).removesuffix(".tsp"), cost, f"{elapsed_time:.5f}", "-"])

            total_cost += cost
            total_time += elapsed_time
            num_files += 1

            print("Evaluated: " + str([os.path.basename(filename).removesuffix(".tsp"), cost, f"{elapsed_time:.5f}", "-"]))

        mean_cost = total_cost / num_files
        mean_time = total_time / num_files
        
        # Write the mean values at the end
        writer.writerow(["Mean", mean_cost, f"{mean_time:.5f}", "-"])

if __name__ == "__main__":
    esolver = DynamicProgrammingSolver()
    nearest = NearestNeighborSolver(0)
    greedy = GreedySolver(0)
    randomized = RandomizedSolver(0)
    llm = LLMSolver("gpt-4o")

    for filepath in ["tsp5/tsp5-4.tsp", "tsp10/tsp10-39.tsp", "tsp10/tsp10-43.tsp", "tsp20/tsp20-10.tsp", "tsp20/tsp20-27.tsp"]:
        variance(llm, filepath, "results/variance/LLMSolver-variance-"+os.path.basename(filepath).removesuffix(".tsp")+".csv", 10)
        
    for i in [5, 10, 20]:
        # DynamicProgrammingSolver
        collect_data(esolver, "tsp"+str(i), "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # NearestNeighborSolver
        collect_data(nearest, "tsp"+str(i), "results/tsp"+str(i)+"/NearestNeighborSolver-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # GreedySolver
        collect_data(greedy, "tsp"+str(i), "results/tsp"+str(i)+"/GreedySolver-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # RandomizedSolver
        collect_data(randomized, "tsp"+str(i), "results/tsp"+str(i)+"/RandomizedSolver-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # LLMSolver
        collect_data(llm, "tsp"+str(i), "results/tsp"+str(i)+"/LLMSolver-gpt-4o-tsp"+str(i)+".csv", "results/tsp"+str(i)+"/DynamicProgrammingSolver-tsp"+str(i)+".csv")

        # RL

    for i in [30]:
        # NearestNeighborSolver
        collect_data_no_opt(nearest, "tsp"+str(i), "results/tsp"+str(i)+"/NearestNeighborSolver-tsp"+str(i)+".csv")

        # GreedySolver
        collect_data_no_opt(greedy, "tsp"+str(i), "results/tsp"+str(i)+"/GreedySolver-tsp"+str(i)+".csv")

        # RandomizedSolver
        collect_data_no_opt(randomized, "tsp"+str(i), "results/tsp"+str(i)+"/RandomizedSolver-tsp"+str(i)+".csv")

        # LLMSolver
        collect_data_no_opt(llm, "tsp"+str(i), "results/tsp"+str(i)+"/LLMSolver-gpt-4o-tsp"+str(i)+".csv")

        #