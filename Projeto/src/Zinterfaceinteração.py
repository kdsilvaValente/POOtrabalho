import sys
from Auxiliares_uteis import *
from AbstractMenu import *
from User import *
from Search import*  
from bson.objectid import ObjectId




    
  
class Interface_interação(Menu):    
    def init_interação(self, user: str, user_pesquisa: str ) -> str:
        self.search = Search("User")
        self.next = "0"
        if user_pesquisa == None:
            self.user = User(user)
            self.options()
        else:
            self.ver_perfil(user_pesquisa)
        return self.next

    
    
    def options(self):
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
                        print("aqui")
                        return 
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 3.")
            except ValueError:
                print("Digite um número válido.")
    
    def display_main_menu(self):
        print("1. Ver lista de amigos")
        print("2. Ver lista de pedidos de amizade")
        print("3. Voltar")
        print("-------------------------------")
    
    def display_main_menu_option(self, option):
        if option == 1:
            self.ver_amigos()
        elif option == 2:
            self.ver_pedidos()
        elif option == 3:
            self.next = "Perfil"
     
        
    
    def ver_perfil(self, id):
        result=self.search.get_by_id(ObjectId(id))
        print(f"Nome:{result['name']}")
        print(f"Gênero:{result['gender']}")
        if result['isonline'] == False:
            print(f"Status: offline")
        else:
            print(f"Status: online")
        while True:
            try:
                option = int(input("Deseja pedir amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.pedir_amizade(id)
                    else:
                        self.next = "Amizades"  
                        return 0
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")


    def pedir_amizade(self, id):
        self.user.pedir_amizade(id)
        print("Pedido realizado com sucesso!")
        self.next="Amizades"
    
    def aceitar_amizade(self, amizades):
        escolha=int(input("Qual amizade você deseja aceitar?: "))
        self.user.aceitar_pedido(amizades[escolha-1])
  
    
    def ver_amigos(self):
        length=len(self.user.lista_amigos)
        for i in range(length):
            result=self.search.get_by_id(ObjectId(self.user.lista_amigos[i]))
            print(f"{[i+1]}:{result['name']}")
        self.amigos(self.user.lista_amigos)

    def amigos(self,friends ):
        print("-------------------------------")
        print("1. Ver perfil de algum amigo")
        print("2. desfazer amizade com algum amigo")
        print("3. voltar")
        print("-------------------------------")
        while True:
            try:
                option=int(input())
                if 1 <= option <= 3:
                    if option == 1:
                        option = int(input("Qual perfil deseja ver? Digite o número: "))
                        self.ver_perfil(friends[option-1])
                        return 0
                    else:
                        self.next = "Amizades"  
                        return 0
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")


        
    
    def ver_pedidos(self):
        length=len(self.user.lista_pedidos)
        for i in range(length):
            result=self.search.get_by_id(ObjectId(self.user.lista_pedidos[i]))
            print(f"{[i+1]}:{result['name']}")
        while True:
            try:
                option = int(input("Deseja aceitar alguma amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.aceitar_amizade(self.user.lista_pedidos)
                    else:
                        self.next = "Amizades"  
                        return 0
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")

    def excluir_amigo(self,id):
        self.user.excluir_amigo(id)
        print("Amizade desfeita!")
    
    def render(self):
        self.title = "INTERAÇÃO"
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

# # Example usage
# teste = Interface_interação()
# teste.init_interação("6670f0d789c9d0cd1ce88f79")
# teste.options()
