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
