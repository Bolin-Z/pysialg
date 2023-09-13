from abc import ABC, abstractmethod
from math import pi, cos, exp, sqrt

class Function(ABC):
    def __init__(
            self,
            lb:list[float],
            ub:list[float],
            minimize:bool = True
        ) -> None:
        self.lb = lb
        self.ub = ub
        self.D = len(lb)
        self.minimize = minimize
    
    def fitter(self, fvalA:float, fvalB:float) -> bool:
        """return whether A is fitter than B
        """
        if self.minimize:
            return fvalA < fvalB
        else:
            return fvalA > fvalB
    
    @abstractmethod
    def evaluate(self, solution:list[float]) -> float:
        pass

# Rastrigin function
class Ackley(Function):
    def evaluate(self, solution: list[float]) -> float:
        a = 20
        b = 0.2
        c = 2 * pi
        d = self.D
        alpha = 0.0
        beta = 0.0
        for x in solution:
            alpha += (x ** 2)
            beta += cos(c *x)
        return - a * exp(-b * sqrt(alpha / d)) - exp(beta / d) + a + exp(1)