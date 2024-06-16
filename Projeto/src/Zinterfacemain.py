from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca
from connection_options.connection import DBconnectionHandler # import run para testa conexão 


class Interface_main:
    def __init__(self) -> None:
        self.next = None
        self.user = None
        self.interface_user = None
        self.interface_login = None
        self.navegação = "Navegação"
        self.perfil = "Perfil"
        self.sair = "Sair"
        self.db_handle= DBconnectionHandler()
        self.db_handle.connect_to_db()


    def initial_menu(self)  -> None:  # Menu principal
        while True:
            try:
                self.verificar_conexão()
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

    def login(self) -> None:
        limpar_terminal()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        user = self.interface_login .login()
        if user:
            self.user = user
            self.user_menu()
    def logout(self):
        self.interface_login.logout()
        self.next = None
        self.user = None
        self.interface_user = None
        self.interface_login = None 
        limpar_terminal       
        self.initial_menu

        

    def create_profile(self) -> None:
        limpar_terminal()
        self.interface_user = User_interface()
        self.interface_user.init_user(None)

    def user_menu(self):
        limpar_terminal()
        self.interface_user = User_interface()
        self.next = self.interface_user.init_user(self.user)
        if self.next == self.navegação:
            self.search_menu()
        if self.next == self.sair:
            self.logout()
            
        

    def search_menu(self) -> None:
        limpar_terminal()
        interface_search = Interface_search() #pelo metodo de super não estava dando certo
        self.next=interface_search.init_search() # o return deve ser o resultado do id e também o número da próxima ação
        if self.next == self.perfil:
            self.user_menu()
    def verificar_conexão(self):
        if  self.db_handle.connect_to_db() == True:
            return 0
        else:
            print("Falha na conexão, tente novamente mais tarde ou verifique sua conexão com a internet")






main_interface = Interface_main()
main_interface.initial_menu()
