"""ga.py Genetic Algorithm for TSP
"""
from tools.debug import DEBUG
from random import seed, randrange,shuffle,uniform as rand
from tests.tsp import DirectedWeightedGraph
from copy import deepcopy

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
            pc:float = 0.9,
            pm:float = 0.1,
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
        greedyInitial = round(self.popSize * 0.1)
        for i in range(greedyInitial):
            chromosome = self.population[i]
            chromosome.gene = [c for c in self._nearestNeighborHeuristic()]
        for i in range(greedyInitial, self.popSize):
            chromosome = self.population[i]
            chromosome.gene = [c for c in range(self.g.numOfCities)]
            shuffle(chromosome.gene)
    
    def _evaluation(self) -> None:
        for chromosome in self.population:
            chromosome.tourLength = 0.0
            for i in range(-1, self.g.numOfCities - 1, 1):
                src = chromosome.gene[i]
                dst = chromosome.gene[i + 1]
                chromosome.tourLength += self.g.distance[src][dst]
            chromosome.fitnessVal = 1 / chromosome.tourLength

    def _selection(self) -> None:
        # caculate cumulative probability
        cumulativeProbability:list[float] = []
        sumOfFitness:float = 0.0
        for chromosome in self.population:
            sumOfFitness += chromosome.fitnessVal
        probability:float = 0.0
        for chromosome in self.population:
            probability += chromosome.fitnessVal / sumOfFitness
            cumulativeProbability.append(probability)
        # generate new population
        newPopulation:list[_Chromosome] = []
        for _ in range(self.popSize):
            selected = self.rouletteWheel(cumulativeProbability)
            newPopulation.append(deepcopy(self.population[selected]))
        self.population = newPopulation

    def rouletteWheel(self, cumulativeProbability:list[float]) -> int:
        r = rand(0,1)
        for i in range(self.popSize):
            if r < cumulativeProbability[i]:
                return i

    def _crossover(self) -> None:
        # using partially mapped crossover operator
        first:int = -1
        for i in range(self.popSize):
            if rand(0,1) < self.pc:
                if first != -1:
                    # cross over
                    p1Gene = self.population[first].gene
                    p2Gene = self.population[i].gene
                    c1Gene = [0.0 for _ in range(self.g.numOfCities)]
                    c2Gene = [0.0 for _ in range(self.g.numOfCities)]

                    crossPoint1 = randrange(0, self.g.numOfCities)
                    crossPoint2 = randrange(0, self.g.numOfCities)
                    if crossPoint1 > crossPoint2:
                        crossPoint1, crossPoint2 = crossPoint2, crossPoint1
                    # mapping
                    p1top2 = {}
                    p2top1 = {}
                    # cross
                    for k in range(crossPoint1, crossPoint2 + 1):
                        c1Gene[k] = p2Gene[k]
                        c2Gene[k] = p1Gene[k]
                        p1top2[p2Gene[k]] = p1Gene[k]
                        p2top1[p1Gene[k]] = p2Gene[k]
                    # repair
                    curIdx = (crossPoint2 + 1) % self.g.numOfCities
                    for _ in range(self.g.numOfCities - (crossPoint2 + 1 - crossPoint1)):
                        target1 = p1Gene[curIdx]
                        target2 = p2Gene[curIdx]
                        if target1 in p1top2:
                            target1 = p1top2[target1]
                            while target1 in p1top2:
                                target1 = p1top2[target1]
                        if target2 in p2top1:
                            target2 = p2top1[target2]
                            while target2 in p2top1:
                                target2 = p2top1[target2]
                        c1Gene[curIdx] = target1
                        c2Gene[curIdx] = target2
                        curIdx = (curIdx + 1) % self.g.numOfCities
                    # finish
                    self.population[first].gene = c1Gene
                    self.population[i].gene = c2Gene
                    first = -1
                else:
                    first = i

    def _mutation(self) -> None:
        # simply swap two genes
        for chromosome in self.population:
            if rand(0,1) < self.pm:
                # mutation
                r1 = randrange(0, self.g.numOfCities)
                r2 = randrange(0, self.g.numOfCities)
                while r2 == r1:
                    r2 = randrange(0, self.g.numOfCities)
                chromosome.gene[r1], chromosome.gene[r2] = chromosome.gene[r2], chromosome.gene[r1]

    def _updategBest(self) -> None:
        curBest = self.population[0]
        for i in range(self.popSize):
            chromosome = self.population[i]
            if chromosome.tourLength < curBest.tourLength:
                curBest = self.population[i]
        if curBest.tourLength < self.gBestLength:
            self.gBestTour = [c for c in curBest.gene]
            self.gBestTour.append(self.gBestTour[0])
            self.gBestLength = curBest.tourLength
    
    def printResult(self) -> None:
        """print the best tour and its length
        """
        for i in range(len(self.gBestTour)):
            if i == len(self.gBestTour) - 1:
                print(self.gBestTour[0] + 1)
            else:
                print(self.gBestTour[i] + 1, end=" -> ")
        print(f"length: {self.gBestLength}")
    
    def _nearestNeighborHeuristic(self) -> list[int]:
        visited = []
        unvisited = {c for c in range(self.g.numOfCities)}
        visited.append(randrange(0, self.g.numOfCities))
        unvisited.discard(visited[0])
        while len(unvisited) != 0:
            nextCity = None
            minLength = None
            for c in unvisited:
                if nextCity == None:
                    nextCity = c
                    minLength = self.g.distance[visited[-1]][nextCity]
                else:
                    length = self.g.distance[visited[-1]][c]
                    if length < minLength:
                        nextCity = c
                        minLength = length
            visited.append(nextCity)
            unvisited.discard(nextCity)
        return visited
        