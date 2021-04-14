import random
import numpy as np
from deap import creator, base, tools, algorithms

rng = np.random.default_rng()
loads = [27, 7, 6, 5, 4, 6, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 27, 7, 6, 5, 4, 6, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
POP_SIZE = 11
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_bool", lambda: rng.integers(2))

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(loads))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', tools.cxOnePoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=0.5)


def sel_elite_tournament(individuals, k_elitist, k_tournament, tournsize):
    return tools.selBest(individuals, k_elitist) + tools.selTournament(individuals, k_tournament, tournsize=2)


toolbox.register('select', sel_elite_tournament, k_elitist=1, k_tournament=POP_SIZE - 1, tournsize=2)


def eval_balance(individual):
    ind1, ind2 = 0, 0
    for i, v in enumerate(individual):
        if v == 0:
            ind1 += loads[i]
        else:
            ind2 += loads[i]
    return abs(ind1 - ind2),


toolbox.register('evaluate', eval_balance)


def main():
    random.seed(64)

    pop = toolbox.population(n=POP_SIZE)
    CXPB, MUTPB = 0.9, 0.5

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("Evaluated %i individuals" % len(pop))
    fits = [ind.fitness.values[0] for ind in pop]
    ngen = 1000
    g = 0

    while min(fits) > 0 and g < ngen:
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
