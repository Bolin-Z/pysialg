"""ga.py Genetic Algorithm for TSP
"""
from tools.debug import DEBUG
from random import seed, uniform as rand
from tests.tsp import DirectedWeightedGraph

class _Chromosome:
    def __init__(self) -> None:
        self.gene:list[float|int] = []
        self.tourLength:float = 0.0
        self.eval:float = 0.0

class GeneticAlgorithm:
    def run(self) -> None:
        # initialization phase
        # main loop
        for _ in range(self.maxGeneration):
            self._evaluation()
            newPopulation = self._selection()
            
    def __init__(
            self,
            graph:DirectedWeightedGraph,
            maxGeneration:int = 1000,
            populationSize:int = 30,
            pc:float = 0.6,
            pm:float = 0.05,
            rdSeed:float = 0xD5F1306
        ) -> None:
        
        # random seed
        seed(rdSeed)
        # termination condition
        self.maxGeneration = maxGeneration
        # problem defined
        self.g = graph
        # population size
        self.popSize = populationSize
        self.pupulation = [_Chromosome() for _ in range(self.popSize)]
        # parameter
        self.pc = pc
        self.pm = pm
        # result
        self.gBestTour = []
        self.gBestLength = None
    
    def _evaluation(self) -> None:
        pass

    def _selection(self) -> list[_Chromosome]:
        pass

    def _crossover(self, population:list[_Chromosome]):
        pass