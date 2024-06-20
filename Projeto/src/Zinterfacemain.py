from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca
from ZInterfaceAdmin import *
from Zinterfaceinteração import*
from ZInterfaceAvaliacaoMusica import * 
from ZInterfaceAvaliacaoAlbum import *
from connection_options.connection import DBconnectionHandler # import run para testa conexão 


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
        self.avaliacaomsc = "Musica"
        self.avaliacaoalbum = "Album"
        self.db_handle= DBconnectionHandler()
        self.db_handle.connect_to_db()
        

    def initial_menu(self)  -> None:  # Menu principal
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
        clear_screen()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        user_id = self.interface_login.login()
        if user_id:
            admin = Admin(user_id)
            if admin.can_modify_admin_status():
                print("Login administrativo bem-sucedido.")
                self.user = admin
                self.admin_menu()
            else:
                print("Acesso negado. Você não possui permissão de administrador.")
        else:
            print("Acesso negado. Usuário não encontrado.")
                
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
    def admin_menu(self):
        clear_screen()
        if self.user is None or not self.user.is_admin:
            print("Acesso negado. Você não possui permissão de administrador.")
            return
        admin_menu = menuAdmin(self.user.user_id)
        while admin_menu.next in ["Musica_edição", "Album_edição"]:
            if admin_menu.next == "Musica_edição":
                self.musica_menu()
            elif admin_menu.next == "Album_edição":
                self.album_menu()
            admin_menu = menuAdmin(self.user.user_id)  # Resetando o menu admin para continuar no loop
        if admin_menu.next == "Sair":
            self.logout()


    def search_menu(self) -> None:
        """
        Controla a abertura da interface de busca e direciona o próximo menu a ser aberto após a busca.
        """
        while self.next == self.navegação:
            self.next= Interface_search() #pelo metodo de super não estava dando certo
            self.next=self.next.next 
            if self.next == self.perfil:
                self.user_menu()
            elif isinstance(self.next, dict):
                if self.next["next"] == self.amizades:
                    self.user_pesquisa = str(self.next["id_pesquisa"])
                    self.next = self.amizades
                    self.interações_usuários()
                elif self.next["next"] == self.avaliacaoalbum:
                    self.user_pesquisa =  str(self.next["id_pesquisa"] )
                    self.next = self.navegação
                    self.avaliacaoAlbum_menu()
                elif self.next["next"] == self.avaliacaomsc:
                    self.user_pesquisa =  str(self.next["id_pesquisa"] )
                    self.next = self.navegação
                    self.avaliacaoMusica_menu()

    def avaliacaoMusica_menu(self) -> None:
        interfacemusica = AvaliacaoInterMsc(self.user, self.user_pesquisa)
        while interfacemusica.next is None or interfacemusica.next == self.avaliacaomsc:
            interfacemusica.iniciotela()

            if interfacemusica.next == "Navegação":
                self.next = self.navegação
                self.search_menu()

            elif interfacemusica.next == "Perfil":
                self.next = self.perfil
                self.user_menu()

    def avaliacaoAlbum_menu(self) -> None:
        interfacealbum = AvaliacaoInterfaceAlb(self.user, self.user_pesquisa)
        while interfacealbum.next is None or interfacealbum.next == self.avaliacaoalbum:
            interfacealbum.iniciotela()

            if interfacealbum.next == "Navegação":
                self.next = self.navegação
                self.search_menu()
                
            elif interfacealbum.next == "Perfil":
                self.next = self.perfil
                self.user_menu()
        
    def verificar_conexão(self):
        if  self.db_handle.connect_to_db() == True:
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
    
def musica_menu(self):
        musica_menu = menuMusica()
        while musica_menu.next != "Voltar":
            musica_menu.options1()
        self.admin_menu()



main_interface = Interface_main()
main_interface.initial_menu()
