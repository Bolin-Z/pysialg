from tools.debug import DEBUG
from tests.tsp import tsp, DirectedWeightedGraph
from algs.acs import AntColonySystem
from algs.ga import GeneticAlgorithm
from algs.antSystem import AntSystem
from time import time

if __name__ == "__main__":
    DEBUG.ON = True
    g = [
        DirectedWeightedGraph(tsp[1], points2matrix=True),
        DirectedWeightedGraph(tsp[2])
    ]
    choose = 0
    rd = time()
    solver = AntColonySystem(g[choose], rdSeed=rd, maxGeneration=2000)
    solver.run()    
    solver = GeneticAlgorithm(g[choose], rdSeed=rd, maxGeneration=2000)
    solver.run()
    solver = AntSystem(g[choose], rdSeed=rd, maxGeneration=2000)
    solver.run()