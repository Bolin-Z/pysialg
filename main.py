from tools.debug import DEBUG
from tests.tsp import tsp, DirectedWeightedGraph
from algs.acs import AntColonySystem
from algs.ga import GeneticAlgorithm
from time import time

if __name__ == "__main__":
    DEBUG.ON = True
    graph = DirectedWeightedGraph(
        tsp[1], points2matrix=True
    )
    rd = time()
    solver = AntColonySystem(graph, rdSeed=rd)
    solver.run()
    solver = GeneticAlgorithm(graph, rdSeed=rd)
    solver.run()