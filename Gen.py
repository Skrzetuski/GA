import matplotlib.pyplot as plt
import networkx

class Gen:
    def __init__(self,t,i,h):
        self.toolbox = t
        self.individual = i
        self.history = h

    def showGraph(self):
        graph = networkx.DiGraph(self.history.getGenealogy(self.individual))
        graph = graph.reverse()  # Make the graph top-down
        colors = [self.toolbox.evaluate(self.history.genealogy_history[i])[0] for i in graph]
        networkx.draw(graph, node_color=colors)
        plt.show()

    def hideGraph(self):
        plt.close()

