import random
import numpy as np
from deap import creator, base, tools, algorithms

# instances
import db_connection

rng = np.random.default_rng()

# globals
POP_SIZE = 50
C = 23
CXPB, MUTPB = 0.65, 0.2  # Crossover and Mutation probabilities
MUTRT = 0.023
NGEN = 100  # number of generations
K_ELITE = 1
K_TOURNAMENT = 5


creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -0.5))  # define weights
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

toolbox.register("attr_bool", lambda: rng.integers(2))

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, C)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=MUTRT)

toolbox.register('select', tools.selNSGA)


def fitness_func(individual):
    return db_connection.simulate_individual(individual)

toolbox.register('evaluate', fitness_func)


def main():
    random.seed(64)

    pop = toolbox.population(n=POP_SIZE)

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("Evaluated %i individuals" % len(pop))
    fits = [ind.fitness.values[0] for ind in pop]
    g = 0

    while min(fits) > 0 and g < NGEN:
        g += 1
        offspring = toolbox.select(pop)
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if rng.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child1.fitness.values
        for mutant in offspring:
            if rng.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        print('generation %i:' % g)
        print("fitness --", min(fits))

    best_ind = tools.selBest(pop, 1)[0]
    print(best_ind)
    print("fitness --", min(fits))


if __name__ == '__main__':
    main()
