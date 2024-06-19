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
        self.next = "0" #definição do next que será acessado posteriomente pela class main
        self.user = User(user)
        self.title = "INTERAÇÃO"
        if user_pesquisa is None: #verifica se o user_pesquisa é none, pois se for, o usuário não quer ver um perfil específico 
            self.options()
        else:
            self.ver_perfil(user_pesquisa)

    def options(self) -> None:  # menu de opções inicial do perfil, controla a entrada da seleção de opção e chama o menu com as opções
        while self.next == "0": #loop para controle de entrada
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
    
    def display_main_menu(self) -> None:   #printa o menu principal na tela
        print(emoji.emojize("1. Ver lista de amigos :people_hugging:"))
        print(emoji.emojize("2. Ver lista de pedidos de amizade :envelope:"))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        print("-------------------------------")
    
    def display_main_menu_option(self, option: int) -> None:  #direciona a função de acordo com a opção inicial escolhida
        if option == 1:
            self.ver_amigos()
        elif option == 2:
            self.ver_pedidos()
        elif option == 3:
            self.next = "Perfil"
     
    def ver_perfil(self, id: str) -> None: #abre o perfil de algum usuário específico
        result = self.search.get_by_id(ObjectId(id))
        print(f"Nome: {result['name']}")
        print(f"Gênero: {result['gender']}")
        status = "online" if result['isonline'] else "offline"
        print(f"Status: {status}")
        
        while True:#loop para controle de entrada
            try:
                option = int(input("Deseja pedir amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.pedir_amizade(ObjectId(id))
                        return 0
                    else:
                        limpar_terminal()
                        self.next = "Amizades" #define amizades como próximo menu
                        return
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")

    def pedir_amizade(self, id: ObjectId) -> None: #realiza o pedido de amizade a um usuário
        self.user.pedir_amizade(id) # faz a mudança no banco
        print(emoji.emojize("Pedido realizado com sucesso:rocket:!"))
        self.next = "Amizades"
    
    def aceitar_amizade(self, amizades: list) -> None: #aceita o pedido de uma amizade
        while True:
            escolha = int(input("Qual amizade você deseja aceitar?: "))
            if escolha > len(amizades) or escolha < len(amizades):
                 print("Escolha um número de usuário existente!")
            else:
                 self.user.aceitar_pedido(amizades[escolha-1])
                 self.next="Amizades"
                 return 0 

    
    def ver_amigos(self) -> None: #redenriza a lista de amigos do usuário
        if not  self.user.lista_amigos:
            print("você não tem um amigo ainda, continue navegando e faça novas amizades!")
        else:
            length = len(self.user.lista_amigos)
            for i in range(length):
                result = self.search.get_by_id(ObjectId(self.user.lista_amigos[i]))
                print(f"{i+1}: {result['name']}")
            self.amigos(self.user.lista_amigos)

    def amigos(self, friends: list) -> None: #redenriza opções após ver lista de amigos disponíveis
        print("-------------------------------")
        print(emoji.emojize("1. Ver perfil de algum amigo :people_hugging: "))
        print(emoji.emojize("2. Desfazer amizade com algum amigo :cross_mark: "))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        print("-------------------------------")
        while True:
            try:
                option = int(input("Escolha uma opção: ")) #editar para controle entrada maior ou menor
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

    def ver_pedidos(self) -> None: #renderiza os pedidos de amizade
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
                        return 0
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
    
    def render(self) -> None: #render padrão 
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
