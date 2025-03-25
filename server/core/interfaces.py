from abc import ABC, abstractmethod

class ISolver(ABC):
    @abstractmethod
    def __init__(self, objective, constraints, rhs, num_variables):
        pass

    @abstractmethod
    def solve(self):
        pass
