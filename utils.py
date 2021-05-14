import param
import random
from deap import creator, base, tools, algorithms
from Knapsack import Knapsack


def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += param.items[item][0]
        value += param.items[item][1]
    if len(individual) > param.MAX_ITEM or weight > param.MAX_WEIGHT:
        return 10000, 0  # Ensure overweighted bags are dominated
    return weight, value


def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)  # Used in order to keep type
    ind1 &= ind2  # Intersection (inplace)
    ind2 ^= temp  # Symmetric Difference (inplace)
    return ind1, ind2


def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:  # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(param.NBR_ITEMS))
    return individual,


def setupToolbox(toolbox):
    random.seed(64)

    creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", set, fitness=creator.Fitness)

    # Attribute generator
    toolbox.register("attr_item", random.randrange, param.NBR_ITEMS)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_item, param.IND_INIT_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalKnapsack)
    toolbox.register("mate", cxSet)
    toolbox.register("mutate", mutSet)
    toolbox.register("select", tools.selNSGA2)
    return toolbox


def mapGenToKnapsack(individual):
    tmp_knapsack = Knapsack([])
    for item in individual:
        tmp_knapsack.items.append(param.items[item])
    return tmp_knapsack


def getBestIndividual(fits, population):
    for individual in population:
        if individual.fitness.values[1] == max(fits):
            result = individual
    return result


