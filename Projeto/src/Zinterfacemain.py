from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca
from ZInterfaceAdmin import *
from Zinterfaceinteração import*
from connection_options.connection import DBconnectionHandler # import run para testa conexão 


class Interface_main:
    def __init__(self) -> None:
        self.next = None
        self.user = None
        self.user_pesquisa = None
        self.interface_login = None
        self.navegação = "Navegação"
        self.perfil = "Perfil"
        self.sair = "Sair"
        self.admin = "Admin"
        self.amizades = "Amizades"
        self.db_handle= DBconnectionHandler()
        self.db_handle.connect_to_db()


    def initial_menu(self)  -> None:  # Menu principal
        while True:
            try:
                self.verificar_conexão()
                print("Bem-vindo ao albumatic, o que deseja fazer?")
                print("1. Login")
                print("2. Criar perfil")
                print("3. Login como Administrador")

                option = int(input())
                if option == 1:
                    self.login()
                elif option == 2:
                    self.create_profile()
                elif option == 3:
                    self.admin_login()

                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 2:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def login(self) -> None:  # controla a abertura da interface de interações e difereciona o próximo menu a ser aberto
        limpar_terminal()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        user = self.interface_login .login()
        if user:
            self.user = user
            self.user_menu()
    def logout(self):  #desloga o usuário
        limpar_terminal()
        self.interface_login.logout() #função que realiza o log out no banco de dados
        self.next = None
        self.user = None
        self.interface_user = None
        self.interface_login = None 
        self.initial_menu


    def admin_login(self) -> None:  # controla a abertura da interface de login de admin e difereciona o próximo menu a ser aberto
        limpar_terminal()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        admin = self.interface_login.login()  
        if admin and admin.is_admin:  
            self.admin_menu()

    def create_profile(self) -> None: # controla a abertura da interface de criar perfil e difereciona o próximo menu a ser aberto
        limpar_terminal()
        self.interface_user = User_interface(None)
        self.interface_user.init_user()

    def user_menu(self):  # controla a abertura da interface de user e difereciona o próximo menu a ser aberto
        limpar_terminal()
        self.next = User_interface(self.user)
        self.next = self.next.next
        print(self.next)
        if self.next == self.navegação:
            self.search_menu()
        if self.next == self.sair:
            self.logout()
        if self.next == self.amizades:
            self.interações_usuários()

    def admin_menu(self):  # controla a abertura da interface de admin e difereciona o próximo menu a ser aberto
        limpar_terminal()
        menu = menuAdmin()
        while True:
            menu.render()
            try:
                option = int(input())
                menu.next(option)
            except ValueError:
                print("Por favor, insira um número válido.")      

    def search_menu(self) -> None:  # controla a abertura da interface de search e difereciona o próximo menu a ser aberto
        while self.next == self.navegação:
            limpar_terminal()
            self.next= Interface_search() #pelo metodo de super não estava dando certo
            self.next=self.next.next
            if self.next == self.perfil:
                self.user_menu()
            elif isinstance(self.next, dict):
                if self.next["next"] == self.amizades:
                    self.user_pesquisa =  str(self.next["id_pesquisa"] )
                    self.next = self.amizades
                    self.interações_usuários()
   
            

    def verificar_conexão(self): # testando se a conexão existe, para pode iniciar o programas
        if  self.db_handle.connect_to_db() == True:
            return 0
        else:
            print("Falha na conexão, tente novamente mais tarde ou verifique sua conexão com a internet")
    def interações_usuários(self): # controla a abertura da interface de interações e difereciona o próximo menu a ser aberto
        limpar_terminal()
        while self.next == "Amizades" or isinstance(self.next, dict):
            self.next = Interface_interação(self.user, self.user_pesquisa)
            self.next=self.next.next
            self.user_pesquisa = None
            if self.next == self.perfil:
                self.user_menu()
    
          
        



main_interface = Interface_main()
main_interface.initial_menu()
