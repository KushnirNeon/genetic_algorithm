# Genetic Algorithm for Multi-Constrained Knapsack

This project solves a **knapsack problem** with **weight and volume constraints** using a **genetic algorithm** in Python.

---

## Problem

Given `N` items, each with:

- `value`
- `weight`
- `volume`

Select items to **maximize total value** while keeping:

- `total weight ≤ MAX_WEIGHT`
- `total volume ≤ MAX_VOLUME`

---

## Key Features

- **Binary individual representation:** 1 = item selected, 0 = not selected  
- **Fitness function:** total value minus penalties for exceeding constraints  
- **Selection:** tournament (k=3)  
- **Crossover:** one-point (probability 0.9)  
- **Mutation:** flip bit (probability 0.02)  
- **Elitism:** top 2 individuals preserved  

---

## Parameters

```python
N = 50
POP_SIZE = 120
GENERATIONS = 250
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.02
ELITISM = 2
MAX_WEIGHT = 0.4 * sum(weights)
MAX_VOLUME = 0.35 * sum(volumes)
