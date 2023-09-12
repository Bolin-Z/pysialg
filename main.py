from algs.acs import AntColonySystem
from tools.debug import DEBUG
from tests.acstest import tsp
from os import times

if __name__ == "__main__":
    DEBUG.ON = True
    solver = AntColonySystem(
        tsp[2], maxGeneration = 2000
    )
    solver.run()