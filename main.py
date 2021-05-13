import matplotlib.pyplot as plt
import networkx
from Knapsack import Knapsack
from utils import *


def main():
    random.seed(64)
    history = tools.History()

    toolbox = setupToolbox(base.Toolbox())

    toolbox.decorate("mate", history.decorator)
    toolbox.decorate("mutate", history.decorator)

    population = toolbox.population(n=MU)
    history.update(population)
    hof = tools.ParetoFront()

    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,
                              halloffame=hof)

    fits = [ind.fitness.values[1] for ind in population]

    for ind in population:
        if ind.fitness.values[1] == max(fits):
            result = ind

    final_knapsack = Knapsack([])
    for item in result:
        final_knapsack.items.append(items[item])

    print(result)

    print(final_knapsack.items)

    print("History")
    print(history.getGenealogy(result))

    graph = networkx.DiGraph(history.getGenealogy(result))
    graph = graph.reverse()  # Make the graph top-down
    colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    networkx.draw(graph, node_color=colors)
    plt.show()

    return population, hof


if __name__ == "__main__":
    main()
