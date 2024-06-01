from Search import*
import sys #para usar o sys.exit()
from Auxiliares_uteis import*
from bson import ObjectId #biblioteca para poder usar o ObjectId e converter no formato bson



class Interface_search:
    def init_search(self):
        self.data=[]
        self.result=[]
        self.options_value=0
    def options(self):
        while True:
            try:
                limpar_terminal()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                self.options_value=option
                if 1 <= option <= 4:
                     if option !=4:
                        self.display_main_menu_option(option)
                     else:
                        print("Encerrando o programa.") 
                        sys.exit()#corrigindo bug de encerrar programanda
                               
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 4.")
            except ValueError:
                print("Digite um número válido.")
    def display_main_menu(self):
        print("-------------------------------")
        print('O que deseja pesquisar?')
        print("1. Música")
        print("2. Produtor")
        print("3. Album")
        print("4. Voltar")
        #opções de navegação, e a opção sair precisa direcionar para a tela anterior
    def display_main_menu_option(self,option):
        data=[]
        if option == 1:
            data={
                "collection": "Musica",
                "type": "titulo"
            }
        if option == 2:
            data={
                "collection": "Musica",
                "type": "produtores"
            }
        if option == 3:
            data={
                "collection": "Albuns",
                "type": "album"
            }
        limpar_terminal()
        self.searching(data,option)
    def searching(self,data, option):
        search=Search(data["collection"])
        if option ==1  or option == 2:
            if option == 2:
                name=input(str("Qual o nome do produtor?:"))
            else:
                name=input(str("Qual o nome da música?:"))
            result=search.get_by_type(data["type"],name)
            print("Abaixo segue os resultados correspondentes:")
            self.print_musica(result)
            self.menu_result_musica()
        elif option == 3:
            name=input(str("Qual o nome do album?:"))
            result=search.get_by_type(data["type"],name)
            print("Abaixo segue os resultados correspondentes:")
            self.print_album(result)
            self.menu_result_album()
    
    def print_musica(self, result): #printa os resultados da pesquisa feita  na collection música
        result_lenth=len(result)
        for i in range(result_lenth):
            print(f"{i+1}:")
            print(f"Título: {(result[i])['titulo']}")
            print(f"album: {(result[i])['album']}")
            print(f"artista: {(result[i])['artista']}")
            print(f"gênero: {(result[i])['genero']}")
            print(f"compositores: {(result[i])['compositores']}")
            print(f"produtores: {(result[i])['produtores']}")
        self.result=result

              
    def print_album(self, result): #printa os resultados da pesquisa feita  na collection album
        result_lenth=len(result)
        for i in range(result_lenth):
            print(f"{i+1}:")
            print(f"album: {(result[i])['album']}")
            print(f"artista: {(result[i])['artista']}")
            print(f"gênero: {(result[i])['gênero']}")
            vetor_musicas= result[i]['musicas']
            tamanho=len(vetor_musicas)
            print("Musicas do Album:")
            for i in range(tamanho):
                data={
                "collection": "Musica",
                "type": "_id"
            }
                search=Search(data["collection"])
                musica=search.get_by_id(data["type"])
                print(f"{[i+1]}:{musica[i]['titulo']}")
        self.result=result
    def menu_result_musica(self):
        print('O que deseja fazer?:')
        print("1. Abrir música")
        print("2. Retornar para buscas")
        options = int(input("Escolha uma opção: "))
        self.options_value=options   
        self.result_option_musica()
    def menu_result_album(self):
        print('O que deseja fazer?:')
        print("1. Abrir album")
        print("2. Abrir música do album")
        print("3. Retornar para buscas")
        options = int(input("Escolha uma opção: "))
        self.options_value=options
        self.result_option_album()
    def result_option_album(self):
        if  self.options_value == 1:
            pass
        if  self.options_value == 2:
            pass
        else:
            self.options()
    def result_option_musica(self):
         if  self.options_value == 1:
            return 0
         else:
            self.options()

     
            



                

                    

                




 
    
teste=Interface_search()
teste.options()