import random
import numpy as np

N = 50

values = np.random.randint(5, 100, size=N)
weights = np.random.randint(1, 30, size=N)
volumes = np.random.randint(1, 20, size=N)

MAX_WEIGHT = int(0.4 * weights.sum())
MAX_VOLUME = int(0.35 * volumes.sum())

POP_SIZE = 120
GENERATIONS = 250
TOURNAMENT_K = 3
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.02
ELITISM = 2

def random_individual():
    return np.random.randint(0, 2, size=N)

def decode(ind):
    val = (ind * values).sum()
    w = (ind * weights).sum()
    vol = (ind * volumes).sum()
    return val, w, vol

def fitness(ind):
    val, w, vol = decode(ind)
    penalty = 0
    if w > MAX_WEIGHT:
        penalty += 10 * (w - MAX_WEIGHT)
    if vol > MAX_VOLUME:
        penalty += 12 * (vol - MAX_VOLUME)
    return val - penalty

def tournament_selection(pop, scores, k=TOURNAMENT_K):
    ids = random.sample(range(len(pop)), k)
    best = ids[0]
    for i in ids:
        if scores[i] > scores[best]:
            best = i
    return pop[best].copy()

def one_point_crossover(a, b):
    if random.random() > CROSSOVER_RATE:
        return a.copy(), b.copy()
    pt = random.randint(1, N-1)
    child1 = np.concatenate([a[:pt], b[pt:]])
    child2 = np.concatenate([b[:pt], a[pt:]])  # виправлено
    return child1, child2

def mutate(ind):
    for i in range(N):
        if random.random() < MUTATION_RATE:
            ind[i] = 1 - ind[i]
    return ind

def color_text(val, limit):
    """Підсвічування червоним, якщо перевищено ліміт"""
    if val > limit:
        return f"\033[91m{val}\033[0m"
    else:
        return str(val)

# ====================== Генетичний алгоритм ======================
population = [random_individual() for _ in range(POP_SIZE)]
best_history = []
best_overall = None
best_score = -10**9
progress_log = []

for gen in range(GENERATIONS):
    scores = np.array([fitness(ind) for ind in population])
    idx_best = int(np.argmax(scores))
    if scores[idx_best] > best_score:
        best_score = scores[idx_best]
        best_overall = population[idx_best].copy()
    best_history.append(best_score)

    if gen % 25 == 0 or gen == GENERATIONS-1:
        progress_log.append((gen, best_score))

    sorted_idx = np.argsort(-scores)
    new_pop = [population[i].copy() for i in sorted_idx[:ELITISM]]
    while len(new_pop) < POP_SIZE:
        parent1 = tournament_selection(population, scores)
        parent2 = tournament_selection(population, scores)
        child1, child2 = one_point_crossover(parent1, parent2)
        child1 = mutate(child1)
        if len(new_pop) < POP_SIZE:
            new_pop.append(child1)
        if len(new_pop) < POP_SIZE:
            child2 = mutate(child2)
            new_pop.append(child2)
    population = new_pop

val, w, vol = decode(best_overall)

print(f"Best fitness (with penalties applied): {best_score:.2f}")
print(f"Total value = {val}")
print(f"Total weight = {color_text(w, MAX_WEIGHT)}/{MAX_WEIGHT}")
print(f"Total volume = {color_text(vol, MAX_VOLUME)}/{MAX_VOLUME}")

selected = np.where(best_overall == 1)[0]
print("\nSelected items (highlighted if over limits):")
print("Index | Value | Weight | Volume")
for i in selected:
    w_i = color_text(weights[i], MAX_WEIGHT)
    v_i = color_text(volumes[i], MAX_VOLUME)
    print(f"{i:5d} | {values[i]:5d} | {w_i:6} | {v_i:6}")

weight_pct = w / MAX_WEIGHT * 100
volume_pct = vol / MAX_VOLUME * 100
print(f"\nWeight usage: {w}/{MAX_WEIGHT} ({weight_pct:.1f}%)")
print(f"Volume usage: {vol}/{MAX_VOLUME} ({volume_pct:.1f}%)")

print("\nProgress (best fitness every 25 generations):")
for gen, score in progress_log:
    print(f"Generation {gen:4d}: {score:.2f}")

