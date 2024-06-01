from AbstractMenu import *
from Albuns import *
from Excel import * 

class menuMusica(Menu):
    def __init__(self):
        self.title = "Menu Albuns :p"
        self.options = [
            "1 - Adicionar um album",
            "2 - Editar album",
            "3 - Apagar album",
            "4 - Exibir albuns do banco",
            "5 - Ler Excel novamente"
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