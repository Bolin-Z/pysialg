from algs.acs import AntColonySystem, DirectedWeightedGraph
from tools.debug import DEBUG
from time import time
from tests.tsp import tsp
from algs.de import DifferentialEvolution
from tests.functions import Ackley
from algs.pso import ParticleSwarmOptimization

if __name__ == "__main__":
    DEBUG.ON = True
    D = 30
    f = Ackley(
        [-32.768 for _ in range(D)],
        [ 32.768 for _ in range(D)]
    )
    r = time()
    solver = DifferentialEvolution(f, populationSize=5*D,maxGeneration=2000,rdSeed=r)
    solver.run()
    solver = ParticleSwarmOptimization(f, populationSize=5*D,maxGeneration=2000, rdSeed=r)
    solver.run()