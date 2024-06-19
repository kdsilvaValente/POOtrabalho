from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca
from ZInterfaceAdmin import *
from Zinterfaceinteração import*
from connection_options.connection import DBconnectionHandler # Import run para testar conexão 


class Interface_main:
    """
    Classe principal que gerencia a interface do sistema e a navegação entre os menus.
    """
    def __init__(self) -> None:
        """
        Inicializa os atributos da classe e estabelece conexão com o banco de dados.
        """
        self.next = None
        self.user = None
        self.user_pesquisa = None
        self.interface_login = None
        self.navegação = "Navegação"
        self.perfil = "Perfil"
        self.sair = "Sair"
        self.admin = "Admin"
        self.amizades = "Amizades"
        self.login_menu = "login"
        self.db_handle = DBconnectionHandler()
        self.db_handle.connect_to_db()

    def initial_menu(self) -> None:
        """
        Método que exibe o menu principal do sistema.
        """
        while True:
            try:
                self.verificar_conexão()
                print("Bem-vindo ao albumatic, o que deseja fazer?")
                print("1. Login")
                print("2. Criar perfil")
                print("3. Realizar ação como Administrador")

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

    def login(self) -> None:
        """
        Controla a abertura da interface de interações e direciona o próximo menu a ser aberto após o login.
        """
        limpar_terminal()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        user = self.interface_login.login()
        if user:
            self.user = user
            self.user_menu()

    def logout(self) -> None:
        """
        Desloga o usuário e retorna ao menu inicial.
        """
        limpar_terminal()
        self.interface_login.logout()  # Função que realiza o logout no banco de dados
        self.next = None
        self.user = None
        self.interface_user = None
        self.interface_login = None 
        self.initial_menu()

    def admin_login(self) -> None:
        """
        Controla a abertura da interface de login de administrador e direciona o próximo menu a ser aberto após o login.
        """
        limpar_terminal()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        admin = Admin(self.interface_login.login())
        if admin:
            print("Login administrativo bem-sucedido.")
            self.admin_menu()
        else:
            print("Acesso negado. Você não possui permissão de administrador.")
            
    def create_profile(self) -> None:
        """
        Controla a abertura da interface de criação de perfil e direciona o próximo menu a ser aberto após a criação.
        """
        limpar_terminal()
        self.interface_user = User_interface(None)

    def user_menu(self) -> None:
        """
        Controla a abertura da interface de usuário e direciona o próximo menu a ser aberto.
        """
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
        if self.next == self.login_menu:
            self.login()

    def admin_menu(self) -> None:
        """
        Controla a abertura da interface de administrador e direciona o próximo menu a ser aberto.
        """
        limpar_terminal()
        menu = menuAdmin()
        while True:
            menu.render()
            try:
                option = int(input())
                menu.next(option)
            except ValueError:
                print("Por favor, insira um número válido.")      

    def search_menu(self) -> None:
        """
        Controla a abertura da interface de busca e direciona o próximo menu a ser aberto após a busca.
        """
        while self.next == self.navegação:
            limpar_terminal()
            self.next = Interface_search()  # Pelo método de super não estava dando certo
            self.next = self.next.next
            if self.next == self.perfil:
                self.user_menu()
            elif isinstance(self.next, dict):
                if self.next["next"] == self.amizades:
                    self.user_pesquisa = str(self.next["id_pesquisa"])
                    self.next = self.amizades
                    self.interações_usuários()
   
    def verificar_conexão(self) -> None:
        """
        Testa se a conexão com o banco de dados existe antes de iniciar o programa.
        """
        if self.db_handle.connect_to_db():
            return 0
        else:
            print("Falha na conexão, tente novamente mais tarde ou verifique sua conexão com a internet")

    def interações_usuários(self) -> None:
        """
        Controla a abertura da interface de interações de usuários e direciona o próximo menu a ser aberto.
        """
        limpar_terminal()
        while self.next == "Amizades" or isinstance(self.next, dict):
            self.next = Interface_interação(self.user, self.user_pesquisa)
            self.next = self.next.next
            self.user_pesquisa = None
            if self.next == self.perfil:
                self.user_menu()

main_interface = Interface_main()
main_interface.initial_menu()
