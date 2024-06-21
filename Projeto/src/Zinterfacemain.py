from Zinterfacelogin import *  # Importando interface de login
from ZInterfaceuser import *   # Importando interface de usuário
from Zinterfacesearch import *  # Importando interface de busca
from ZInterfaceAdmin import *
from Zinterfaceinteração import*
from ZInterfaceAvaliacaoMusica import * 
from ZInterfaceAvaliacaoAlbum import *
from connection_options.connection import DBconnectionHandler # import run para testa conexão 
import sys
import emoji

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
        self.musica_edicao = "Musica_edição"
        self.album_edicao = "Album_edição"
        self.login_menu = "login"
        self.db_handle= DBconnectionHandler()
        self.db_handle.connect_to_db()
        

    def initial_menu(self)  -> None:  # Menu principal
        while True:
            try:
                self.verificar_conexão()
                print("Bem-vindo ao albumatic, o que deseja fazer?")
                print(emoji.emojize("1. Login:partying_face:"))
                print(emoji.emojize("2. Criar perfil:exploding_head: "))
                print(emoji.emojize("3. Realizar ação como Administrador:nerd_face:"))
                print(emoji.emojize("4. Encerrar programa:loudly_crying_face:"))


                option = int(input())
                if option == 1:
                    self.login()
                elif option == 2:
                    self.create_profile()
                elif option == 3:
                    self.admin_login()
                elif option == 4:
                    limpar_terminal()
                    print("encerrando Albumagic...")
                    sys.exit()
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
        self.user = self.interface_login.login()
        if self.user:
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
        """
        Controla a abertura da interface de login de administrador e direciona o próximo menu a ser aberto após o login.
        """
        clear_screen()
        self.verificar_conexão()
        self.interface_login = Interface_login()
        user_id = self.interface_login.login()
        
        if user_id:
            try:
                admin = Admin(user_id)
                if admin.can_modify_admin_status():  # Verifica se o usuário logado é administrador
                    print("Login administrativo bem-sucedido.")
                    self.user = admin
                    self.admin_menu()
                else:
                    print("Acesso negado. Você não possui permissão de administrador.")
            except PermissionError as e:
                print(e)  # Exibe a mensagem de erro de permissão
        else:
            print("Acesso negado. Usuário não encontrado.")
                
    def create_profile(self) -> None:
        """
        Controla a abertura da interface de criação de perfil e direciona o próximo menu a ser aberto após a criação.
        """
        self.verificar_conexão()
        limpar_terminal()
        self.interface_user = User_interface(None)

    def user_menu(self) -> None:
        
        """
        Controla a abertura da interface de usuário e direciona o próximo menu a ser aberto.
        """
        limpar_terminal()
        self.verificar_conexão()
        self.next = User_interface(self.user)
        self.next = self.next.next
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
        
        clear_screen()
        if self.user is None or not self.user.is_admin:
            print("Acesso negado. Você não possui permissão de administrador.")
            return
        
        self.next = menuAdmin(self.user.user_id)
        self.next = self.next.next
        if self.next == "Musica_edição":
                self.musica_menu()
        elif self.next == "Album_edição":
                self.album_menu()
        elif self.next == "Sair":
                self.logout()      


    def search_menu(self) -> None:
        """
        Controla a abertura da interface de busca e direciona o próximo menu a ser aberto após a busca.
        """
        limpar_terminal()
        self.verificar_conexão()
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
        limpar_terminal()
        self.verificar_conexão()
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
        limpar_terminal()
        self.verificar_conexão()
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
            sys.exit()

    def interações_usuários(self) -> None:
        """
        Controla a abertura da interface de interações de usuários e direciona o próximo menu a ser aberto.
        """
        limpar_terminal()
        self.verificar_conexão()
        while self.next == "Amizades" or isinstance(self.next, dict):
            self.next = Interface_interação(self.user, self.user_pesquisa)
            self.next = self.next.next
            self.user_pesquisa = None
            if self.next == self.perfil:
                self.user_menu()
    
    def musica_menu(self) -> None:

        '''
        método de interface para acessar o menu musica
        '''
        
        clear_screen()
        menu_musica = menuMusica()  

        while menu_musica.next != "Voltar":
            menu_musica.options1()  
        
        self.admin_menu()


    def album_menu(self):
        
        '''
        método de interface para acessar o menu album
        '''

        clear_screen()
        menu_album = menuAlbum()  
        while menu_album.next != "Voltar":
            menu_album.options1()  
        
        self.admin_menu()



main_interface = Interface_main()
main_interface.initial_menu()
