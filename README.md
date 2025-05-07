# csci538-tsp
 A final project for CSCI 538 focused on solving the Traveling Salesman Problem using various methods.

 ## Graph Format
```
NAME: example
TYPE: TSP
DIMENSION: 5
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 10 20
2 30 40
3 50 10
4 60 60
5 70 20
EOF
```

This .tsp file format is based off the [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) format.

## Dataset
The dataset used to test algorithms was randomly generated using the generate_data.py script. The tsp5, tsp10, tsp20, and tsp30 directories include 50 TSP instances each with 5, 10, 20, and 30 nodes, respectively. This dataset was used for testing each algorithm to ensure replicability and validity.

## Explantation of Scripts
### graph.py
Saves and loads .tsp files in TSPLIB format and generates synthetic graphs for TSP solvers. Handles graph format, methods, and validation.

### generate_data.py
This generates a synthetic dataset of TSP instances as set of .tsp files.

### evaluate.py
This runs the solvers on the tsp5, tsp10, tsp20, and tsp30 instances to collect metrics including cost, time (s), optimality gap (%). It is also used to collect data on the variation of direct LLM solver solutions on the same TSP instance.

## Solvers
### exact.py
Implements python_tsp library to solve TSP instances using dynamic programming.

### heuristic.py
Implements nearest neighbor, greedy, and randomized heuristic algorithms for solving TSP instances.

### llm_solver.py
Uses the OpenAI Assistants API to solve TSP instances. Below is the prompt given to the assistant:
```
You are a TSP (Traveling Salesman Problem) solver. I will give you a TSP instance in standard TSPLIB format using EUC_2D (Euclidean 2D distances). Your task is to return a good enough tour — a list of node IDs in the order they should be visited. Solve this TSP problem using best-effort reasoning, not exact computation. Try to find the optimal but return a best guess if the problem is too complex to solve optimally.

Formatting rules:
- If you can solve the problem, return ONLY the tour in this exact format: [1, 2, 3, 4, 5]
- Do not include any explanation, formatting, or notes before or after the list.
- The tour must be a complete Hamiltonian cycle (returns to the starting node implicitly).
- If you cannot solve it for any reason, first return this exact line:  
failure  
Then, on the next line, provide a clear explanation in a short paragraph why it failed.

Here is the TSP instance format:

NAME: example  
TYPE: TSP  
DIMENSION: 5  
EDGE_WEIGHT_TYPE: EUC_2D  
NODE_COORD_SECTION  
1 10 20  
2 30 40  
3 50 10  
4 60 60  
5 70 20  
EOF
```

### TSPRLAgent
Implements GAT + RL with pytorch to solve TSP intances.