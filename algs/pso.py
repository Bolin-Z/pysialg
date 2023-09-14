"""pso.py Particle Swarm Optimization
"""
from tools.debug import DEBUG
from random import seed, uniform as rand
from tests.functions import Function

class Particle:
    def __init__(self, dimensio:int) -> None:
        self.x = [0.0 for _ in range(dimensio)]
        self.fx:float = None
        self.pBest = [0.0 for _ in range(dimensio)]
        self.fpBest:float = None
        self.v = [0.0 for _ in range(dimensio)]
    
    def updatepBest(self) -> None:
        self.pBest = [i for i in self.x]
        self.fpBest = self.fx

class ParticleSwarmOptimization:
    def run(self) -> None:
        DEBUG.PRINT("----- Particle Swarm Optimization -----")
        # main loop
        for _ in range(self.maxGeneration):
            gBest = self.swarm[self.gBestIdx]
            # update each particle
            for i in range(self.popSize):
                p = self.swarm[i]
                for d in range(self.dim):
                    # update velocity
                    p.v[d] = self.w * p.v[d] + self.c1 * rand(0,1) * (p.pBest[d] - p.x[d]) \
                                + self.c2 * rand(0,1) * (gBest.pBest[d] - p.x[d])
                    p.v[d] = max(-self.vmax[d], min(p.v[d], self.vmax[d]))
                    # update position
                    p.x[d] = p.x[d] + p.v[d]
                    p.x[d] = max(self.lb[d], min(p.x[d], self.ub[d]))
                # evaluate
                p.fx = self.f(p.x)
                # update pBest
                if self.fitter(p.fx, p.fpBest):
                    p.updatepBest
                    # update gBest
                    if self.fitter(p.fpBest, gBest.fpBest):
                        self.gBestIdx = i

        # get the result
        self.gBest = [i for i in self.swarm[self.gBestIdx].x]
        self.gBestVal = self.swarm[self.gBestIdx].fpBest

        if DEBUG.ON:
            print(f"Best Val: {self.gBestVal}")
            print(f"Solution: {self.gBest}")
        
        DEBUG.PRINT("--------------- Finish ----------------")

    def __init__(
            self,
            objectFunction:Function,
            populationSize:int = 30,
            c1:float = 2.0,
            c2:float = 2.0,
            w:float = 0.9,
            vmaxPercent:float = 0.2,
            maxGeneration:int = 1000,
            rdSeed:float = 0xD5F1306
        ) -> None:
        
        # random seed
        seed(rdSeed)
        # termination condition
        self.maxGeneration = maxGeneration
        # target funciton
        self.f = objectFunction.evaluate
        self.fitter = objectFunction.fitter
        self.dim = objectFunction.D
        self.lb = objectFunction.lb
        self.ub = objectFunction.ub
        self.vmax = [vmaxPercent * (self.ub[x] - self.lb[x]) for x in range(self.dim)]
        # population
        self.popSize = populationSize
        self.swarm:list[Particle] = []
        for _ in range(self.popSize):
            newParticle = Particle(self.dim)
            for d in range(self.dim):
                newParticle.x[d] = rand(self.lb[d], self.ub[d])
                newParticle.v[d] = rand(-self.vmax[d], self.vmax[d])
            newParticle.fx = self.f(newParticle.x)
            newParticle.updatepBest()
            self.swarm.append(newParticle)
        # parameter
        self.c1 = c1
        self.c2 = c2
        self.w = w
        # result
        self.gBestIdx:int = 0
        self.gBest:list[float] = []
        self.gBestVal:float = 0.0

        for i in range(self.popSize):
            if self.fitter(self.swarm[i].fpBest, self.swarm[self.gBestIdx].fpBest):
                self.gBestIdx = i