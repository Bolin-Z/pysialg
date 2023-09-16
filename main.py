from tools.debug import DEBUG
from tests.tsp import tsp, DirectedWeightedGraph
from algs.acs import AntColonySystem
from algs.ga import GeneticAlgorithm

if __name__ == "__main__":
    DEBUG.ON = True
    graph1 = DirectedWeightedGraph(
        tsp[1], points2matrix=True
    )
    graph2 = DirectedWeightedGraph(tsp[2])

    solver = AntColonySystem(graph2)
    solver.run()    
    solver = GeneticAlgorithm(graph2)
    solver.run()