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

# menu Principal com opções e a função 'next' para escolher o próximo menu
class MainMenu(Menu):
    def __init__(self):
        self.title = "Menu Principal :p"
        self.options = [
            "1 - Configurações de usuario",
            "2 - Opções de avaliação de música",
            "3 - Consultar album",
            "4 - Ler comentários de músicas",
        ]

    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)

        print("\n>> Digite sua opção")

    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        if option == 1:
            print("Exibindo opções de configurações de usuario...")
            # vai retornar uma instância do classe filha do menu correspondente correspondente em todas opções abaixo
        elif option == 2:
            print("Exibindo opções de avaliação de música...")
        elif option == 3:
            print("Vamos consultar as faixas de um album!")
        elif option == 4:
            print("Vamos ler o que as pessoas tem dito sobre essa música...")
        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  