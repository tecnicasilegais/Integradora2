import random
import logging
import numpy as np
from deap import creator, base, tools, algorithms
import util

# instances
import db_connection

rng = np.random.default_rng()

# globals
POP_SIZE = 50
C = 22
CXPB, MUTPB = 0.65, 0.2  # Crossover and Mutation probabilities
MUTRT = 0.023
NGEN = 100  # number of generations
K_ELITE = 1
K_TOURNAMENT = 5
db = db_connection.Db()

logging.basicConfig(filename=util.make_filename('gen_execution.log'), encoding='utf-8', level=logging.DEBUG)

creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -0.5))  # define weights
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

toolbox.register("attr_bool", lambda: rng.integers(2))

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, C)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=MUTRT)

toolbox.register('select', tools.selNSGA2)


def fitness_func(individual):
    return db.simulate_individual(individual)


toolbox.register('evaluate', fitness_func)


def stop_criteria(best_fits):
    return np.all(best_fits == best_fits[0])


def main():
    best_fits = []
    random.seed(64)
    pop = toolbox.population(n=POP_SIZE)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    '''for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("Evaluated %i individuals" % len(pop))
    fits = [ind.fitness.values[0] for ind in pop]
    g = 0'''

    pop = toolbox.select(pop, len(pop))

    # Begin the generational process
    for gen in range(1, NGEN):

        # Vary the population
        offspring = tools.selTournamentDCD(pop, K_TOURNAMENT)
        offspring = [toolbox.clone(ind) for ind in offspring]

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if rng.random() <= CXPB:
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

        pop = toolbox.select(pop + offspring, POP_SIZE)
        fits = [ind.fitness.values[0] for ind in pop]

        print('generation %i:' % gen)
        bestf = min(fits)
        print("fitness --", bestf)

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
