"""antSystem.py Ant System
"""
from tools.debug import DEBUG
from random import seed, random, randrange
from tests.tsp import DirectedWeightedGraph

class _GraphWithPheromone:
    def __init__(self, dwg:DirectedWeightedGraph) -> None:
        self.distance = dwg.distance
        self.numOfCities = dwg.numOfCities
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

class AntSystem:
    def run(self) -> None:
        # initialization phase
        self._nearestNeighborHeuristic()
        self.tao0 = self.numberOfAnts / self.gBestLength
        self.g.pheromone = [[self.tao0 for _ in range(self.g.numOfCities)] for _ in range(self.g.numOfCities)]

        # main loop
        for _ in range(self.maxGeneration):
            # cities to be visited
            for k in range(self.numberOfAnts):
                for c in range(self.g.numOfCities):
                    self.ants[k].toBeVisted.add(c)
            # select a starting city for ant k
            for k in range(self.numberOfAnts):
                self.ants[k].tour.append(randrange(0, self.g.numOfCities))
                self.ants[k].toBeVisted.discard(self.ants[k].tour[0])
            # build tours
            for k in range(self.numberOfAnts):
                for _ in range(self.g.numOfCities - 1):
                    self._randomProportionalRule(k)
            # go back to initial point
            for ant in self.ants:
                ant.tour.append(ant.tour[0])
                ant.tourLength += self.g.distance[ant.tour[-2]][ant.tour[-1]]
            # global pheromone updating
            self._globalPheromoneUpdateingRule()
            # reset the state of ants
            for ant in self.ants:
                ant.reset()

        if DEBUG.ON:
            print("---------- AS ----------")
            self.printResult()
            print("------------------------")

    def __init__(
            self,
            graph:DirectedWeightedGraph,
            maxGeneration:int = 1000,
            numberOfAnts:int = 10,
            alpha:int = 1,
            beta:int = 2,
            rho:float = 0.5,
            rdSeed:float = 0xD5F1306
        ) -> None:
        
        # random seed
        seed(rdSeed)
        # termination condition
        self.maxGeneration = maxGeneration
        # problem defined
        self.g = _GraphWithPheromone(graph)
        # ants colony
        self.numberOfAnts = numberOfAnts
        self.ants = [_Ant() for _ in range(self.numberOfAnts)]
        # parameter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.tao0 = 0.0
        # result
        self.gBestTour = []
        self.gBestLength = None
    
    def _randomProportionalRule(self, curAnt:int) -> None:
        ant = self.ants[curAnt]
        curCity = ant.tour[-1]
        temp = []
        for nextCity in ant.toBeVisted:
            temp.append([
                nextCity,
                ((self.g.pheromone[curCity][nextCity]) ** self.alpha) * ((1 / self.g.distance[curCity][nextCity]) ** self.beta)
            ])
        
        total = 0.0
        for i in range(len(temp)):
            if temp[i][1] == 0:
                print(f"0: {curCity} -> {temp[i][0]}")
                exit()
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
    
    def _globalPheromoneUpdateingRule(self) -> None:
        # evaporate
        for i in range(self.g.numOfCities):
            for j in range(self.g.numOfCities):
                self.g.pheromone[i][j] = (1 - self.rho) * self.g.pheromone[i][j]
                self.g.pheromone[i][j] = max(self.g.pheromone[i][j], self.tao0)
        # release
        for ant in self.ants:
            for i in range(self.g.numOfCities):
                src = ant.tour[i]
                dst = ant.tour[i + 1]
                self.g.pheromone[src][dst] += (1 / ant.tourLength)

    def _nearestNeighborHeuristic(self) -> None:
        """return the tour length produced by the nearest neighbor heuristic
        """
        visited = []
        unvisited = {c for c in range(self.g.numOfCities)}

        visited.append(randrange(0, self.g.numOfCities))
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
        for i in range(len(self.gBestTour)):
            if i == len(self.gBestTour) - 1:
                print(self.gBestTour[0] + 1)
            else:
                print(self.gBestTour[i] + 1, end=" -> ")
        print(f"length: {self.gBestLength}")
