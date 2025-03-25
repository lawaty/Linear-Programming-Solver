from abc import ABC, abstractmethod

class SimplexSolver(ABC):
    @abstractmethod
    def solve(self, data):
        pass

class BigMSolver(ABC):
    @abstractmethod
    def solve(self, data):
        pass

class TwoPhaseSolver(ABC):
    @abstractmethod
    def solve(self, data):
        pass

class GoalProgrammingSolver(ABC):
    @abstractmethod
    def solve(self, data):
        pass
