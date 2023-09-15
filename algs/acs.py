"""acs.py Ant Colony System
"""
from tools.debug import DEBUG
from random import seed, random, randrange
from math import sqrt
from tests.tsp import DirectedWeightedGraph

class GraphWithPheromone(DirectedWeightedGraph):
    def __init__(self, data: list[list[float]], points2matrix: bool = False) -> None:
        super().__init__(data, points2matrix)
        self.pheromone:list[list[float]] = None

class _Ant:
    def __init__(self) -> None:
        self.toBeVisted:set[int] = set()
        self.tour:list[int] = []
        self.tourLength:float = 0.0
    
    def reset(self) -> None:
        self.toBeVisted.clear()
        self.tour.clear()
        self.tourLength:float = 0.0

class AntColonySystem:
    def run(self) -> None:
        # Initialization phase
        self._nearestNeighborHeuristic()
        self.tao0 = 1 / (self.g.numOfCites * self.gBestLength)
        self.g.pheromone = [[self.tao0 for _ in range(self.g.numOfCites)] for _ in range(self.g.numOfCites)]
        
        # main loop
        for _ in range(self.maxGeneration):
            # reset the state of ants
            for k in range(self.numberOfAnts):
                for c in range(self.g.numOfCites):
                    self.ants[k].toBeVisted.add(c)
            # select a starting city for ant k
            for k in range(self.numberOfAnts):
                self.ants[k].tour.append(randrange(0, self.g.numOfCites))
                self.ants[k].toBeVisted.discard(self.ants[k].tour[0])
            # build tours
            for _ in range(self.g.numOfCites - 1):
                for k in range(self.numberOfAnts):
                    self._pseudoRandomProportionalRule(k)
                # local pheromone updating
                self._localPheromoneUpdateingRule()
            # go back to initial point
            for ant in self.ants:
                ant.tour.append(ant.tour[0])
                ant.tourLength += self.g.distance[ant.tour[-2]][ant.tour[-1]]
            self._localPheromoneUpdateingRule()
            # global pheromone udating
            self._globalPheromoneUpdateingRule()
            # reset the state of ants
            for ant in self.ants:
                ant.reset()

        if DEBUG.ON:
            print("--------- ACS ----------")
            self.printResult()
            print("------------------------")

    def __init__(
            self,
            graph:GraphWithPheromone,
            maxGeneration:int = 1000,
            numberOfAnts:int = 10,
            beta:int = 2,
            q0:float = 0.9,
            alpha:float = 0.1,
            rho:float = 0.1,
            rdSeed:float = 0xD5F1306
        ) -> None:
        
        # random seed
        seed(rdSeed)
        # termination condition
        self.maxGeneration = maxGeneration
        # problem defined
        self.g = graph
        # ants colony
        self.numberOfAnts = numberOfAnts
        self.ants = [_Ant() for _ in range(self.numberOfAnts)]
        # parameter
        self.beta = beta
        self.q0 = q0
        self.alpha = alpha
        self.rho = rho
        self.tao0 = 0.0
        # result
        self.gBestTour = []
        self.gBestLength = None

    def _pseudoRandomProportionalRule(self, curAnt:int) -> None:
        ant = self.ants[curAnt]
        curCity = ant.tour[-1]
        q = random()
        temp = []
        for nextCity in ant.toBeVisted:
            temp.append([
                    nextCity,
                    (self.g.pheromone[curCity][nextCity]) * ((1 / self.g.distance[curCity][nextCity]) ** self.beta)
                ])
        
        if q <= self.q0:
            idx = 0
            for i in range(len(temp)):
                if temp[i][1] > temp[idx][1]:
                    idx = i
            ant.tour.append(temp[idx][0])
            ant.tourLength += self.g.distance[curCity][ant.tour[-1]]
            ant.toBeVisted.discard(ant.tour[-1])
        else:
            total = 0.0
            for i in range(len(temp)):
                total += temp[i][1]
            p = [[temp[i][0], temp[i][1] / total] for i in range(len(temp))]
            s = random()
            pSum = 0.0
            for i in range(len(p)):
                pSum += p[i][1]
                if pSum >= s:
                    ant.tour.append(p[i][0])
                    ant.tourLength += self.g.distance[curCity][ant.tour[-1]]
                    ant.toBeVisted.discard(ant.tour[-1])
                    break

    def _localPheromoneUpdateingRule(self) -> None:
        for ant in self.ants:
            srcCity = ant.tour[-2]
            dstCity = ant.tour[-1]
            self.g.pheromone[srcCity][dstCity] = (1 - self.rho) * self.g.pheromone[srcCity][dstCity] + self.rho * self.tao0

    def _globalPheromoneUpdateingRule(self) -> None:
        bestAntIdx = 0
        # find the best solution in this generation
        for k in range(len(self.ants)):
            if self.ants[k].tourLength < self.ants[bestAntIdx].tourLength:
                bestAntIdx = k
        # compare with the global best
        if self.ants[bestAntIdx].tourLength < self.gBestLength:
            self.gBestTour = [c for c in self.ants[bestAntIdx].tour]
            self.gBestLength = self.ants[bestAntIdx].tourLength
        # update pheromone
        for i in range(len(self.gBestTour) - 1):
            src = self.gBestTour[i]
            dst = self.gBestTour[i + 1]
            self.g.pheromone[src][dst] = (1 - self.alpha) * self.g.pheromone[src][dst] + self.alpha * (1 / self.gBestLength)
        
    def _nearestNeighborHeuristic(self) -> None:
        """return the tour length produced by the nearest neighbor heuristic
        """
        visited = []
        unvisited = {c for c in range(self.g.numOfCites)}

        visited.append(randrange(0, self.g.numOfCites))
        unvisited.discard(visited[0])
        tourLength = 0.0
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
            tourLength += minLength
        tourLength += self.g.distance[visited[-1]][visited[0]]
        visited.append(visited[0])

        self.gBestTour = [c for c in visited]
        self.gBestLength = tourLength
        
        if DEBUG.ON:
            print("--- Greedy Heuristic ---")
            self.printResult()
            print("------------------------")

    def printResult(self) -> None:
        """print the best tour and its length
        """
        for i in self.gBestTour:
            print(i + 1, end=" -> ")
        print()
        print(f"length: {self.gBestLength}")