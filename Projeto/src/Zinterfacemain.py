from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca

class Interface_main:
    def __init__(self) -> None:
        self.next = None
        self.user = None
        self.interface_user = None
        self.interface_login = None
        self.navegação = "Navegação"
        self.perfil = "Perfil"



    def initial_menu(self):  # Menu principal
        while True:
            try:
                print("Bem-vindo ao albumatic, o que deseja fazer?")
                print("1. Login")
                print("2. Criar perfil")
                option = int(input())
                if option == 1:
                    self.login()
                elif option == 2:
                    self.create_profile()
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")

    def login(self):
        self.interface_login = Interface_login()
        user = self.interface_login .login()
        if user:
            self.user = user
            self.user_menu()

    def create_profile(self):
        self.interface_user = User_interface()
        self.interface_user.init_user(None)

    def user_menu(self):
        self.interface_user = User_interface()
        next_action = self.interface_user.init_user(self.user)
        if next_action == 1:
            self.search_menu()

    def search_menu(self):
        interface_search = Interface_search() #pelo metodo de super não estava dando certo
        next_action=interface_search.init_search() # o return deve ser o resultado do id e também o número da próxima ação
        if next_action == self.perfil:
            self.user_menu()






main_interface = Interface_main()
main_interface.initial_menu()
