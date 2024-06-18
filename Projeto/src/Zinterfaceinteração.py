import sys
from Auxiliares_uteis import *
from AbstractMenu import *
from User import *
from Search import*  
from bson.objectid import ObjectId
import emoji


class Interface_interação(Menu):
    def __init__(self, user: str, user_pesquisa: str = None) -> str:
        super().__init__()
        self.search = Search("User")
        self.next = "0"
        self.user = User(user)
        self.title = "INTERAÇÃO"
        if user_pesquisa is None:
            self.options()
        else:
            self.ver_perfil(user_pesquisa)

    def options(self) -> None:
        while self.next == "0":
            try:
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                print("-------------------------------")
                if 1 <= option <= 3:
                    if option != 3:
                        self.display_main_menu_option(option)
                    else:
                        self.next = "Perfil"
                        print("Voltando ao perfil...")
                        return 
                else:
                   print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 3:prohibited: "))
            except ValueError:
                print("Digite um número válido.")
    
    def display_main_menu(self) -> None:
        print(emoji.emojize("1. Ver lista de amigos :people_hugging:"))
        print(emoji.emojize("2. Ver lista de pedidos de amizade :envelope:"))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        print("-------------------------------")
    
    def display_main_menu_option(self, option: int) -> None:
        if option == 1:
            self.ver_amigos()
        elif option == 2:
            self.ver_pedidos()
        elif option == 3:
            self.next = "Perfil"
     
    def ver_perfil(self, id: str) -> None:
        result = self.search.get_by_id(ObjectId(id))
        print(f"Nome: {result['name']}")
        print(f"Gênero: {result['gender']}")
        status = "online" if result['isonline'] else "offline"
        print(f"Status: {status}")
        
        while True:
            try:
                option = int(input("Deseja pedir amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.pedir_amizade(ObjectId(id))
                        return 0
                    else:
                        limpar_terminal()
                        self.next = "Amizades"
                        return
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")

    def pedir_amizade(self, id: ObjectId) -> None:
        self.user.pedir_amizade(id)
        print(emoji.emojize("Pedido realizado com sucesso:rocket:!"))
        self.next = "Amizades"
    
    def aceitar_amizade(self, amizades: list) -> None:
        escolha = int(input("Qual amizade você deseja aceitar?: "))
        self.user.aceitar_pedido(amizades[escolha-1])
    
    def ver_amigos(self) -> None:
        length = len(self.user.lista_amigos)
        for i in range(length):
            result = self.search.get_by_id(ObjectId(self.user.lista_amigos[i]))
            print(f"{i+1}: {result['name']}")
        self.amigos(self.user.lista_amigos)

    def amigos(self, friends: list) -> None:
        print("-------------------------------")
        print(emoji.emojize("1. Ver perfil de algum amigo :people_hugging: "))
        print(emoji.emojize("2. Desfazer amizade com algum amigo :cross_mark: "))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        print("-------------------------------")
        while True:
            try:
                option = int(input("Escolha uma opção: "))
                if 1 <= option <= 3:
                    if option == 1:
                        perfil = int(input("Qual perfil deseja ver? Digite o número: "))
                        self.ver_perfil(friends[perfil-1])
                        return
                    elif option == 2:
                        amizade = int(input("Qual amizade deseja desfazer? Digite o número: "))
                        self.excluir_amigo(friends[amizade-1])
                        return
                    else:
                        limpar_terminal()
                        self.next = "Amizades"  
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 3:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def ver_pedidos(self) -> None:
        length = len(self.user.lista_pedidos)
        for i in range(length):
            result = self.search.get_by_id(ObjectId(self.user.lista_pedidos[i]))
            print(f"{i+1}: {result['name']}")
        
        while True:
            try:
                if not self.user.lista_pedidos:
                    print("Você não tem nenhum pedido ainda, continue navegando e faça amigos!")
                    option = 2
                else:
                    option = int(input("Deseja aceitar alguma amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.aceitar_amizade(self.user.lista_pedidos)
                    else:
                        self.next = "Amizades"
                        return
                else:
                   print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 2:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def excluir_amigo(self, id: ObjectId) -> None:
        self.user.excluir_amigo(id)
        print("Amizade desfeita!")
    
    def render(self) -> None:
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
