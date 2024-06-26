import sys  # para usar o sys.exit()
from Auxiliares_uteis import *
from bson import ObjectId  # biblioteca para poder usar o ObjectId e converter no formato bson
from Search import Search  
from AbstractMenu import *
import emoji


class Interface_search(Menu):
    """
    Classe que gerencia a interface de busca e navegação do sistema.
    """
    def __init__(self) -> None:
        """
        Inicializa os atributos da classe e exibe as opções de busca.
        """
        self.vetor_musicas =0
        self.result = []  # armazena os resultados de pesquisa
        self.id_result = None  # armazena o id escolhido a partir do resultado
        self.options_value = 0  # usado para salvar a opção escolhida no menu
        self.next = "Navegação"  # definição do next que será acessado posteriormente pela classe main
        self.musicas_album = []  # armazena os ids da música de um álbum 
        self.pessoas_result = []  # armazena os ids das pessoas resultantes em uma pesquisa
        self.title = "NAVEGAÇÃO"
        self.dicionario = {}
        self.options()

    def render(self) -> None:
        """
        Método de renderização padrão da interface.
        """
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

    def options(self) -> str:
        """
        Menu de opções inicial da interface, controla a entrada da seleção de opção e chama o menu com as opções.
        """
        while True:  # loop para controle de entrada
            try:
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                self.options_value = option
                if 1 <= option <= 5:
                    if option != 5:
                        self.display_main_menu_option(option)
                    else:
                        self.next = "Perfil"  # chave para próximo menu
                        return 0
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 4:prohibited: "))
            except ValueError:
                print("Digite um número válido.")
            return 0

    def display_main_menu(self) -> None:
        """
        Exibe o menu principal na tela.
        """
        printando_divisão()
        print(emoji.emojize('O que deseja pesquisar?:star-struck:'))
        print(emoji.emojize("1. Música:musical_keyboard:"))
        print(emoji.emojize("2. Artista:performing_arts:"))
        print(emoji.emojize("3. Album:headphone:"))
        print(emoji.emojize("4. Pessoas:rainbow_flag:"))
        print((emoji.emojize("5. Voltar :BACK_arrow: ")))
        self.next = "Navegação"

    def display_main_menu_option(self, option: int) -> None:
        """
        Direciona a função de acordo com a opção inicial escolhida.
        """
        data = {}  # data será composta de acordo com a escolha para acessar coleções específicas
        if option == 1:
            data = {
                "collection": "Musica",
                "type": "titulo"
            }
        elif option == 2:
            data = {
                "collection": "Musica",
                "type": "artista"
            }
        elif option == 3:
            data = {
                "collection": "Albuns",
                "type": "album"
            }
        elif option == 4:
            data = {
                "collection": "User",
                "type": "name"
            }
        
        self.searching(data, option)

    def searching(self, data: dict, option: int) -> None:
        """
        Realiza a pesquisa de acordo com a opção escolhida.
        """
        search = Search(data["collection"])
        if option == 1 or option == 2:
            if option == 2:
                name = input("Qual o nome do Artista?: ")
            else:
                name = input("Qual o nome da música?: ")
            result = search.get_by_type(data["type"], name)
            if not result:
                print("Não foi encontrado resultados, tente novamente")
            else:
                print("Abaixo segue os resultados correspondentes:")
                self.print_musica(result) 
                self.menu_result_musica()
        elif option == 3:
            name = input("Qual o nome do álbum?: ")
            result = search.get_by_type(data["type"], name)
            if not result:
                print("Não foi encontrado resultados, tente novamente")
            else:
                print("Abaixo segue os resultados correspondentes:")
                self.print_album(result)
                self.menu_result_album()
        elif option == 4:
            name = input("Qual o nome da pessoa?: ")
            result = search.get_by_type(data["type"], name)
            if not result:
                print("Não foi encontrado resultados, tente novamente")
            else:
                print("Abaixo segue os resultados correspondentes:")
                self.print_pessoas(result)
                self.menu_result_pessoa()

    def print_musica(self, result: list[dict[str, str]]) -> None:
        """
        Exibe os resultados da pesquisa feita na coleção música.
        """
        result_length = len(result)
        for i in range(result_length):
            printando_divisão()
            print(f"{i + 1}:")
            print(f"Título: {(result[i])['titulo']}")
            print(f"Artista: {(result[i])['artista']}")
            printando_divisão()
        self.result = result

    def print_album(self, result: list[dict[str, str]]) -> None:
        """
        Exibe os resultados da pesquisa feita na coleção álbum.
        """
        result_length = len(result)
        for i in range(result_length):
            print(f"{i + 1}:")
            print(f"Álbum: {(result[i])['album']}")
            print(f"Artista: {(result[i])['artista']}")
            print(f"Gênero: {(result[i])['gênero']}")
        self.result = result

    def menu_result_musica(self) -> None:
        """
        Exibe as opções de ação com os resultados de músicas.
        """
        print('O que deseja fazer?:')
        print("1. Abrir música")
        print(emoji.emojize("2. Voltar :BACK_arrow: "))
        while True:
            options = int(input("Escolha uma opção: "))
            if options <1 or options>2:
                print("escolha uma opção válida")
            else:
                self.options_value = options
                self.result_option_musica()
                return 0
        

    def menu_result_album(self) -> None:
        """
        Exibe as opções de ação com os resultados de álbuns.
        """
        print('O que deseja fazer?:')
        print("1. Abrir álbum")
        print("2. Abrir música do álbum")
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        while True:
            options = int(input("Escolha uma opção: "))
            if options <1 or options>3:
                print("escolha uma opção válida")
            else:
                self.options_value = options
                self.result_option_album()
                return 0      
        

    def result_option_album(self) -> int:
        """
        Realiza a ação nos álbuns pesquisados conforme a opção escolhida.
        """
        if self.options_value == 1:
            while True:
                number= int(input("Qual album? Digite o número:"))
                if not testar_tamanho_vetor(len(self.result), number):
                    pass
                else:
                    self.id_result = (self.result[number-1])['_id']
                    self.dicionario = {"next": "Album","id_pesquisa": self.id_result}
                    self.next = self.dicionario
                    print("entrou na search album")
                    return 0
        elif self.options_value == 2:
            while True:
                number = int(input("Qual o álbum? Digite o número: "))
                if not testar_tamanho_vetor(len(self.result), number):
                    pass
                else:
                    self.musicas_album = self.result[number - 1]['musicas']
                    tamanho = len( self.musicas_album )
                    for j in range(tamanho):  
                        data = {
                            "collection": "Musica",
                            "type": "_id"
                        }
                        search = Search(data["collection"])
                        music = search.get_by_id(ObjectId( self.musicas_album [j]))
                        print(f"{j + 1}° {music['titulo']}")
                    while True:
                        music = int(input("Qual música deseja abrir?: "))
                        if not testar_tamanho_vetor(len(self.musicas_album), music):
                            pass
                        else:
                            self.id_result = self.musicas_album[music-1]
                            self.dicionario = {"next": "Musica","id_pesquisa": self.id_result}
                            self.next = self.dicionario
                            self.id_result = self.musicas_album[music - 1]
                            limpar_terminal()
                            return 0
        elif self.options_value == 3:
            return 0
            
            
        else:
            self.options()  # Retornar para buscas

    def result_option_musica(self) -> int:
        """
        Realiza a ação nos resultados de músicas conforme a opção escolhida.
        """
        if self.options_value == 1:
            while True:
                number= int(input("Qual música? Digite o número:"))
                if not testar_tamanho_vetor(len(self.result) ,number):
                    pass
                else:
                    self.id_result = (self.result[number-1])['_id']
                    self.dicionario = {"next": "Musica","id_pesquisa": self.id_result}
                    self.next = self.dicionario
                    limpar_terminal()
                    return 0
            else:
                self.options()  # Retornar para buscas

    def print_pessoas(self, result: list[dict[str, str]]) -> None:
        """
        Exibe os resultados da pesquisa feita na coleção pessoas.
        """
        result_length = len(result)
        for i in range(result_length):
            print(f"{i + 1}: {result[i]['name']}")
        self.pessoas_result = result

    def menu_result_pessoa(self): 
        """
        escolhendo o que fazer com os resultados da pesquisa das pessoas
        """
        print('O que deseja fazer?:')
        print("1. Ver perfil de um usuário")
        print(emoji.emojize("2. Voltar :BACK_arrow: "))
        while True:
                self.options_value = int(input("Escolha uma opção: "))
                if self.options_value <1 or self.options_value>2:
                    print("escolha uma opção válida")
                else:
                     self.result_option_pessoa()
                     return 0

    def result_option_pessoa(self): 
        """
        escolhendo qual perfil deve sofrer a ação
        """
        if self.options_value == 1:
            while True:
                number= int(input("Qual perfil? Digite o número:"))
                if not testar_tamanho_vetor(len(self.pessoas_result), number):
                    pass
                else:
                    self.id_result = ((self.pessoas_result[number-1])['_id'])
                    self.dicionario = {"next": "Amizades",
                                    "id_pesquisa":self.id_result }
                    self.next = self.dicionario
                    limpar_terminal()
                    return 0

                
       


        
        

# teste= Interface_search()
# teste.init_search()