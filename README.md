# csci538-tsp
 A final project for CSCI 538 focused on solving the Traveling Salesman Problem

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

## Explantation of Files
### graph.py
Imports or generates synthetic graphs for TSP solvers. Handles graph formats, methods, and validation.

### llm_solver.py
Uses the OpenAI API to solve TSP instances.