import logging
import random

import numpy as np
from deap import creator, base, tools
from sort import SortingAlgorithms
from strsimpy.weighted_levenshtein import WeightedLevenshtein

import db_connection
import util

# instances
import db_connection
import util

rng = np.random.default_rng()

# globals
POP_SIZE = 50
C = 22
CXPB, MUTPB = 0.65, 0.2  # Crossover and Mutation probabilities
MUTRT = 0.022
NGEN = 100  # number of generations
K_ELITE = 1
K_TOURNAMENT = 5

logging.basicConfig(filename='logs\\' + util.make_filename('gen_execution.log'), level=logging.DEBUG)

db = db_connection.Db(logging)

creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0))  # define weights
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

toolbox.register("attr_bool", lambda: rng.integers(2))

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, C)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=MUTRT)

toolbox.register('select', tools.selNSGA2)


def fitness_func(individual): return db.simulate_individual(individual)


toolbox.register('evaluate', fitness_func)


def stop_criteria(best_fits): return len(set(best_fits)) == 1


def sort_closest_ind(comparer, reference, comparisons):
    res = [0] * len(comparisons)
    for i in range(0, len(comparisons)):
        res[i] = (comparer.distance(reference, comparisons[i][1]), comparisons[i][1])

    res = SortingAlgorithms.quick_sort(res, 0, len(res) - 1)

    return res


def sort_sequence(levenshtein, pop):
    res = [0] * len(pop)
    remaining = sort_closest_ind(levenshtein, [0] * len(pop[0]), list(zip(res, pop)))
    res[0] = remaining[0][1]
    for i in range(1, len(pop)):
        remaining = sort_closest_ind(levenshtein, remaining[0][1], remaining[1:])
        res[i] = remaining[0][1]
    return res


def substitute_cost(a, b): return 2.0 if (a == '0' and b == '1') else 1.0


def main():
    best_fits = []
    random.seed(64)
    pop = toolbox.population(n=POP_SIZE)

    levenshtein = WeightedLevenshtein(substitution_cost_fn=substitute_cost)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values[0] for ind in pop]
    logging.debug('initial:\n')
    for i in range(len(pop)):
        logging.debug('%i: %s' % (i, pop[i]))
        logging.debug('%i: %s' % (i, fits[i]))

    pop = toolbox.select(pop, len(pop))

    # Begin the generational process
    for gen in range(1, NGEN):

        # Vary the population
        offspring = tools.selBest(pop, 1) + tools.selTournamentDCD(pop, K_TOURNAMENT)

        offspring += pop[len(offspring):]

        offspring = [toolbox.clone(ind) for ind in offspring]

        offspring = sort_sequence(levenshtein, offspring)

        print(len(offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if rng.random() <= CXPB:
                # logging.debug('crossover %i' % gen)

                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child1.fitness.values

        for mutant in offspring:
            if rng.random() < MUTPB:
                # logging.debug('mutation %i' % gen)
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(pop + offspring, POP_SIZE)
        pop = sort_sequence(levenshtein, pop)
        fits = [ind.fitness.values[0] for ind in pop]

        '''logging.debug('G %i:' % gen)
        for i in range(len(pop)):
            logging.debug('%i: %s' % (i, pop[i]))
            #logging.debug('%i: %s' % (i, fits[i]))'''

        bestf = min(fits)

        best_ind = tools.selBest(pop, 1)[0]
        logging.info('Generation: %i, best individual: %s, fitness: %s' % (gen, best_ind, bestf))
        best_fits.append(bestf)

        if len(best_fits) > 10:
            best_fits = best_fits[-10:]
            if stop_criteria(best_fits):
                logging.info('Stop criteria reached')
                break

    best_ind = tools.selBest(pop, 1)[0]
    print(best_ind)
    print(min(fits))
    logging.info('END RESULT: best individual: %s, fitness: %s' % (best_ind, min(fits)))


if __name__ == '__main__':
    main()
