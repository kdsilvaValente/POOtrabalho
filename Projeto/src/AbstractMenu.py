from abc import ABC, abstractmethod
import os


# classe abstrata para menus
class Menu(ABC):
    @abstractmethod
    def render(self):
        pass

class InterfaceAvaliacao(ABC):
    @abstractmethod
    def render(self):
        pass
    @abstractmethod
    def iniciotela(self):
        pass
    @abstractmethod
    def next1(self):
        pass
    