"""ga.py Genetic Algorithm for TSP
"""
from tools.debug import DEBUG
from random import seed, shuffle,uniform as rand
from tests.tsp import DirectedWeightedGraph

class _Chromosome:
    def __init__(self) -> None:
        self.gene:list[float|int] = None
        self.tourLength:float = 0.0
        self.fitnessVal:float = 0.0

class GeneticAlgorithm:
    def run(self) -> None:
        # initialization phase
        self._initialPopulation()
        self._evaluation()
        self._updategBest()
        # main loop
        for _ in range(self.maxGeneration):
            self._selection()
            self._crossover()
            self._mutation()
            self._evaluation()
            self._updategBest()
        
        if DEBUG.ON:
            print("---------- GA ----------")
            self.printResult()
            print("------------------------")
            
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
        self.population = [_Chromosome() for _ in range(self.popSize)]
        # parameter
        self.pc = pc
        self.pm = pm
        # result
        self.gBestTour = []
        self.gBestLength = float('inf')
    
    def _initialPopulation(self) -> None:
        for chromosome in self.population:
            chromosome.gene = [c for c in range(self.g.numOfCites)]
            shuffle(chromosome.gene)
    
    def _evaluation(self) -> None:
        for chromosome in self.population:
            chromosome.tourLength = 0.0
            for i in range(-1, self.g.numOfCites - 1, 1):
                src = chromosome.gene[i]
                dst = chromosome.gene[i + 1]
                chromosome.tourLength += self.g.distance[src][dst]
            chromosome.fitnessVal = 1 / chromosome.tourLength

    def _selection(self) -> None:
        p = 0.0
        cp = []
        for i in range(self.popSize):
            pass

    def rouletteWheel(self) -> int:
        pass

    def _crossover(self) -> None:
        pass

    def _mutation(self) -> None:
        pass

    def _updategBest(self) -> None:
        curBest = self.population[0]
        for i in range(self.popSize):
            chromosome = self.population[i]
            if chromosome.tourLength < curBest.tourLength:
                curBest = self.population[i]
        if curBest.tourLength < self.gBestLength:
            self.gBestTour = [c for c in curBest.gene]
            self.gBestLength = curBest.tourLength
    
    def printResult(self) -> None:
        """print the best tour and its length
        """
        for i in self.gBestTour:
            print(i + 1, end=" -> ")
        print()
        print(f"length: {self.gBestLength}")