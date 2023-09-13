from algs.acs import AntColonySystem, DirectedWeightedGraph
from tools.debug import DEBUG
from tests.tsp import tsp
from time import time

if __name__ == "__main__":
    DEBUG.ON = True
    solver = AntColonySystem(
        DirectedWeightedGraph(tsp[2]), maxGeneration=500, rdSeed=time()
    )
    solver.run()