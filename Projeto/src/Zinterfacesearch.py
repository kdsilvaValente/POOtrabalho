import sys  # para usar o sys.exit()
from Auxiliares_uteis import *
from bson import ObjectId  # biblioteca para poder usar o ObjectId e converter no formato bson
from Search import Search  
from AbstractMenu import *
import emoji



class Interface_search(Menu):
    def __init__(self)->None:
        self.data = []
        self.result = []
        self.id_result = None
        self.options_value = 0
        self.next = "0"
        self.musicas_album = []
        self.pessoas_result = []
        self.title = "NAVEGAÇÃO"
        self.dicionario = {}
        self.options()
    
    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

    def options(self) -> str:
        while True:
            try:
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                self.options_value = option
                if 1 <= option <= 5:
                    if option != 5:
                        self.display_main_menu_option(option)
                    else:
                        self.next="Perfil" #chave para próximo menu
                        return 0
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 4:prohibited: "))
            except ValueError:
                print("Digite um número válido.")
            return 0

    def display_main_menu(self):
        print("-------------------------------")
        print('O que deseja pesquisar?')
        print("1. Música")
        print("2. Produtor")
        print("3. Album")
        print("4. Pessoas")
        print(emoji.emojize("5. Voltar :BACK_arrow: "))
        # opções de navegação, e a opção sair precisa direcionar para a tela anterior

    def display_main_menu_option(self, option: int)-> None:
        data = {}
        if option == 1:
            data = {
                "collection": "Musica",
                "type": "titulo"
            }
        elif option == 2:
            data = {
                "collection": "Musica",
                "type": "produtores"
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
        search = Search(data["collection"])
        if option == 1 or option == 2:
            if option == 2:
                name = input("Qual o nome do produtor?: ")
            else:
                name = input("Qual o nome da música?: ")
            result = search.get_by_type(data["type"], name)
            print("Abaixo segue os resultados correspondentes:")
            self.print_musica(result)
            self.menu_result_musica()
        elif option == 3:
            name = input("Qual o nome do album?: ")
            result = search.get_by_type(data["type"], name)
            print("Abaixo segue os resultados correspondentes:")
            self.print_album(result)
            self.menu_result_album()
        elif option == 4:
            name = input("Qual o nome da pessoa?: ")
            result = search.get_by_type(data["type"], name)
            print("Abaixo segue os resultados correspondentes:")
            self.print_pessoas(result)
            self.menu_result_pessoa()

    def print_musica(self, result: list[dict[str, str]])-> None:  # printa os resultados da pesquisa feita na collection música
        result_length = len(result)
        for i in range(result_length):
            print("-------------------------------")
            print(f"{i + 1}:")
            print(f"Título: {(result[i])['titulo']}")
            print(f"album: {(result[i])['album']}")
            print(f"artista: {(result[i])['artista']}")
            print(f"gênero: {(result[i])['genero']}")
            print(f"compositores: {(result[i])['compositores']}")
            print(f"produtores: {(result[i])['produtores']}")
            print("-------------------------------")
        self.result = result

    def print_album(self, result: list[dict[str, str]])->None:  # printa os resultados da pesquisa feita na collection album
        result_length = len(result)
        for i in range(result_length):
            print(f"{i + 1}:")
            print(f"album: {(result[i])['album']}")
            print(f"artista: {(result[i])['artista']}")
            print(f"gênero: {(result[i])['gênero']}")
            vetor_musicas = result[i]['musicas']
            tamanho = len(vetor_musicas)
            print("Musicas do Album:")
            for j in range(tamanho):  
                data = {
                    "collection": "Musica",
                    "type": "_id"
                }
                search = Search(data["collection"])
                music=search.get_by_id(ObjectId(vetor_musicas[j]))
                print(f"{j+1}°{music['titulo']}")
        self.result = result

    def menu_result_musica(self)->None:
        print('O que deseja fazer?:')
        print("1. Abrir música")
        print(emoji.emojize("2. Voltar :BACK_arrow: "))
        options = int(input("Escolha uma opção: "))
        self.options_value = options
        self.result_option_musica()

    def menu_result_album(self)->None:
        
        print('O que deseja fazer?:')
        print("1. Abrir album")
        print("2. Abrir música do album")
        print("3. Visitar perfil")
        print(emoji.emojize("4. Voltar :BACK_arrow: "))
        options = int(input("Escolha uma opção: "))
        self.options_value = options
        self.result_option_album()

    def result_option_album(self) -> int:
        if self.options_value == 1:
            number= int(input("Qual album? Digite o número:"))
            self.id_result = (self.result[number-1])['_id']
            self.dicionario = {"next": "Album","id_pesquisa": self.id_result}
            self.next = self.dicionario
            print("entrou na search album")
            return 0
            
        elif self.options_value == 2:
           number= int(input("Qual o album? Digite o número: "))
           self.musicas_album = self.result[number-1]['musicas']
           music = int(input("Qual música deseja abrir?: "))
           self.id_result = self.musicas_album[music-1]
           limpar_terminal()
           return 0
        elif self.options_value == 3:
           number= int(input("Qual perfil? Digite o número: "))
           self.id_result = self.result[number-1]['_id']
           print(self.id_result)
           limpar_terminal()
           return 0
        else:
            self.options()  # Retornar para buscas

    def result_option_musica(self)->int:
        if self.options_value == 1:
            number= int(input("Qual música? Digite o número:"))
            self.id_result = (self.result[number-1])['_id']
            limpar_terminal()
            return 0
            
        else:
            self.options()  # Retornar para buscas
    
    def print_pessoas(self,result):
        result_length = len(result)
        for i in range(result_length):
             print(f"{i + 1}:{result[i]['name']}")
        self.pessoas_result=result

    def menu_result_pessoa(self):
        print('O que deseja fazer?:')
        print("1. Ver perfil de um usuário")
        print(emoji.emojize("2. Voltar :BACK_arrow: "))
        self.options_value = int(input("Escolha uma opção: "))
        self.result_option_pessoa()

    def result_option_pessoa(self):
         if self.options_value == 1:
            number= int(input("Qual perfil? Digite o número:"))
            print(len(self.pessoas_result))
            self.id_result = ((self.pessoas_result[number-1])['_id'])
            self.dicionario = {"next": "Amizades",
                          "id_pesquisa":self.id_result }
            self.next = self.dicionario
            limpar_terminal()
            return 0
         else:
             self.next = "Navegação"


        
        

# teste= Interface_search()
# teste.init_search()