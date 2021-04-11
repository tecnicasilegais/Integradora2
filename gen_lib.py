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


toolbox.register('select', sel_elite_tournament, k_elitist=1, k_tournament=POP_SIZE-1, tournsize=2)


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
    fits = toolbox.map(toolbox.evaluate, pop)
    for fit, ind in zip(fits, pop):
        ind.fitness.values = fit
    ngen = 1000
    g = 0
    while min(fits) > 0 and g < ngen:
        offspring = algorithms.varAnd(pop, toolbox, cxpb=1.0, mutpb=1.0)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring)
    top10 = tools.selBest(population, k=2)

    for x in top10:
        print(x, eval_balance(x))

if __name__ == '__main__':
    main()

'''    stats = tools.Statistics(lambda ind: ind.fitness.values)
    hof = tools.HallOfFame(1)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    population, log = algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.9, ngen=1000,
                                          stats=stats, halloffame=hof, verbose=True)
    print(hof)
    print(eval_balance(hof))
    return pop, log, hof'''