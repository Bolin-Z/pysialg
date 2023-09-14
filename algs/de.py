"""de.py Differential Evolution
"""
from tools.debug import DEBUG
from random import seed, randrange, sample, uniform as rand
from tests.functions import Function

class DifferentialEvolution:
    def run(self):
        DEBUG.PRINT("------- Differential Evolution --------")
        # main loop
        for _ in range(self.maxGeneration):
            # process each solution
            for i in range(self.popSize):
                # mutation
                trial = [0.0 for _ in range(self.dim)]
                j = randrange(0, self.dim)
                a, b, c = sample([x for x in range(self.popSize) if x != i], k = 3)
                # crossover
                for d in range(self.dim):
                    if rand(0, 1) <= self.CR:
                        trial[d] = self.x[a][d] + self.F * (self.x[b][d] - self.x[c][d])
                    else:
                        trial[d] = self.x[i][d]
                trial[j] = self.x[a][j] + self.F * (self.x[b][d] - self.x[c][d])
                # tail
                for d in range(self.dim):
                    if trial[d] < self.lb[d] or trial[d] > self.ub[d]:
                        trial[d] = rand(self.lb[d], self.ub[d])
                # selection
                fvalT = self.f(trial)
                if self.fitter(fvalT, self.fval[i]):
                    # replace
                    self.x[i] = [k for k in trial]
                    self.fval[i] = fvalT
                    if self.fitter(self.fval[i], self.fval[self.gBestIdx]):
                        self.gBestIdx = i
        # get the result
        self.gBest = [i for i in self.x[self.gBestIdx]]
        self.gBestVal = self.fval[self.gBestIdx]
        
        if DEBUG.ON:
            print(f"Best Val: {self.gBestVal}")
            print(f"Solution: {self.gBest}")
        
        DEBUG.PRINT("--------------- Finish ----------------")

    def __init__(
            self,
            objectFunction:Function,
            populationSize:int,
            F:float = 0.5,
            CR:float = 0.9,
            maxGeneration:int = 1000,
            rdSeed:float = 0xD5F1306
        ) -> None:
        
        # random seed
        seed(rdSeed)
        # termination condition
        self.maxGeneration = maxGeneration
        # target function
        self.f = objectFunction.evaluate
        self.fitter = objectFunction.fitter
        self.dim = objectFunction.D
        self.lb = objectFunction.lb
        self.ub = objectFunction.ub
        # population
        self.popSize = populationSize
        self.x = [[rand(self.lb[i], self.ub[i]) for i in range(self.dim)] for _ in range(self.popSize)]
        self.fval = [self.f(self.x[i]) for i in range(self.popSize)]
        # parameter
        self.F = F
        self.CR = CR
        # result
        self.gBestIdx:int = 0
        self.gBest:list[float] = []
        self.gBestVal:float = 0.0

        for i in range(self.popSize):
            if self.fitter(self.fval[i], self.fval[self.gBestIdx]):
                self.gBestIdx = i
