# Fonte: https://towardsdatascience.com/genetic-algorithm-6aefd897f1ac/

import random


class GeneticAlgorithm:
    def __init__(self, pop_size, crossover_rate, mutation_rate, generations, elitism_size=0):
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.elitism_size = elitism_size

    def select_tournament(self, population, fitnesses, k=3):
        selected = []
        for _ in range(2):
            candidates = random.sample(list(zip(population, fitnesses)), k)
            selected.append(max(candidates, key=lambda x: x[1])[0])
        return selected

    def select_roulette(self, population, fitnesses):
        total_fit = sum(fitnesses)
        if total_fit == 0:
            return random.choices(population, k=2)
        probs = [f / total_fit for f in fitnesses]
        return random.choices(population, weights=probs, k=2)

    def select_truncation(self, population, fitnesses, threshold=0.4):
        sorted_pop = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0], reverse=True)]
        limit = max(1, int(len(sorted_pop) * threshold))
        pool = sorted_pop[:limit]
        return random.choices(pool, k=2)

    def crossover_one_point(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def crossover_two_point(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        point1 = random.randint(1, len(parent1) - 2)
        point2 = random.randint(point1 + 1, len(parent1) - 1)
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2

    def crossover_uniform(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        child1 = []
        child2 = []
        for g1, g2 in zip(parent1, parent2):
            if random.random() < 0.5:
                child1.append(g1)
                child2.append(g2)
            else:
                child1.append(g2)
                child2.append(g1)
        return child1, child2

    def run(self, initialize_fn, fitness_fn, mutate_fn, select_type="tournament", crossover_type="one_point"):
        population = [initialize_fn() for _ in range(self.pop_size)]
        best_ind = None
        best_fit = -1
        history = []

        for gen in range(self.generations):
            fitnesses = [fitness_fn(ind) for ind in population]

            for ind, fit in zip(population, fitnesses):
                if fit > best_fit:
                    best_fit = fit
                    best_ind = ind.copy()

            history.append(best_fit)

            if best_fit >= 1.0:
                break

            new_population = []

            if self.elitism_size > 0:
                sorted_pop = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0], reverse=True)]
                new_population.extend([ind.copy() for ind in sorted_pop[:self.elitism_size]])

            while len(new_population) < self.pop_size:
                if select_type == "tournament":
                    p1, p2 = self.select_tournament(population, fitnesses)
                elif select_type == "roulette":
                    p1, p2 = self.select_roulette(population, fitnesses)
                elif select_type == "truncation":
                    p1, p2 = self.select_truncation(population, fitnesses)
                else:
                    p1, p2 = random.choices(population, k=2)

                if crossover_type == "one_point":
                    c1, c2 = self.crossover_one_point(p1, p2)
                elif crossover_type == "two_point":
                    c1, c2 = self.crossover_two_point(p1, p2)
                elif crossover_type == "uniform":
                    c1, c2 = self.crossover_uniform(p1, p2)
                else:
                    c1, c2 = p1.copy(), p2.copy()

                c1 = mutate_fn(c1, self.mutation_rate)
                c2 = mutate_fn(c2, self.mutation_rate)

                new_population.append(c1)
                if len(new_population) < self.pop_size:
                    new_population.append(c2)

            population = new_population

        return best_ind, best_fit, history
