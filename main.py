import matplotlib.pyplot as plt
import networkx
from utils import *


def main():
    random.seed(64)
    history = tools.History()

    toolbox = setupToolbox(base.Toolbox())

    toolbox.decorate("mate", history.decorator)
    toolbox.decorate("mutate", history.decorator)

    population = toolbox.population(n=MU)
    history.update(population)

    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,
                              verbose=False)

    fits = [ind.fitness.values[1] for ind in population]

    individual = getBestIndividual(fits, population)


    final_knapsack = mapGenToKnapsack(individual)

    print(individual)

    print(final_knapsack.items)

    print("History")
    print(history.getGenealogy(individual))

    graph = networkx.DiGraph(history.getGenealogy(individual))
    graph = graph.reverse()  # Make the graph top-down
    colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    networkx.draw(graph, node_color=colors)
    plt.show()

    return population


if __name__ == "__main__":
    main()
