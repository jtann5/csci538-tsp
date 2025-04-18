# csci538-tsp
 A final project for CSCI 538 focused on solving the Traveling Salesman Problem

 ## Graph Format
```
{
    "nodes": [0, 1, 2, 3],
    "edges": [
        {"from": 0, "to": 1, "weight": 10},
        {"from": 0, "to": 2, "weight": 15},
        {"from": 1, "to": 2, "weight": 20},
        {"from": 2, "to": 3, "weight": 25}
    ]
}
```

## Explantation of Files
### graph.py
Imports or generates synthetic graphs for TSP solvers. Handles graph formats, methods, and validation.

### llm_solver.py
Uses the OpenAI API to solve TSP instances.