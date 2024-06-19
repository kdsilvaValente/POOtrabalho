from abc import ABC, abstractmethod
import os

# define a função para limpar a tela
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    @abstractmethod
    def finalacao(self):
        pass