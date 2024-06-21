from AbstractMenu import *
from Albuns import *
from Excel import * 
from ZInterfaceMusica import *
from Auxiliares_uteis import *

auxiliar = Auxiliar()
excel = Excel()

class menuAlbum(Menu):
    
    def __init__(self):

        '''
        metodo para inicializar a interface
        '''

        self.next = 0
        self.title = "Menu Albuns :p"
        self.options = [
            "1 - Adicionar um album",
            "2 - Editar album",
            "3 - Apagar album",
            "4 - Ler Excel novamente",
            "5 - Voltar"
        ]
        self.options1()

    def options1(self) -> str:
        while True:
            try:
                self.render()
                option = int(input("Escolha uma opção: "))
                self.options_value = option
                if 1 <= option <= 5:
                    if option != 5:
                        self.next1(option)
                    else:
                        self.next = "Voltar"
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 5: "))
            except ValueError:
                print("Digite um número válido.")


    def adicionar_album(self) -> None:
        
        '''
        método de interface para adicionar um álbum ao banco de dados 
        '''
        
        while True:
            
            try:

                clear_screen()
                print("=" * 30)
                print("{:^30}".format("Adicionar Álbum"))
                print("=" * 30) 
                print("")
                print("> Digite as informações do album que deseja adicionar")
                
                album_titulo = str(input("-- Nome: "))
                artista = str(input("-- Artista: "))
                generos_array = str(input("-- Gêneros (separados por vírgula): ")).split(',')
                ano = str(input("-- Ano:"))
                print("")


                album = Albuns(album_titulo, ano, artista, generos_array)
                album.criar_albuns()

                while True:
                    
                    print("> Digite as musicas do álbum:")
                    titulo = str(input("-- Titulo: "))
                    numero = input("-- Numero: ")
                    compositores_array = input("-- Compositores (separados por vírgula): ").split(',')
                    produtores_array = input("-- Produtores (separados por vírgula): ").split(',')
                    duracao = str(input("-- Duração: "))
                    print("")

                    musica = Musica(numero, titulo, artista, album, generos_array, compositores_array, produtores_array, duracao, 0)
                    musica.adicionar_musica()
                
                    adicionar_mais = input("> Deseja adicionar outra música? (s/n): ").strip().lower()
                    if adicionar_mais != 's':
                        album.inserir_musicas_em_albuns()
                        break
                
                adicionar_mais_albuns = input("> Deseja adicionar outro album? (s/n): ").strip().lower()
                if adicionar_mais_albuns != 's':
                    clear_screen()
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")
    

    def editar_album(self) -> None:

        '''
        método de interface para editar informações de um álbum no banco de dados
        '''

        while True:


            try:

                clear_screen()
                print('aaaaaaaaaaaaaaaaaaaa')
                print("Editar album")
                album = str(input("Qual o nome do álbum que você deseja alterar: "))
                id = auxiliar.buscar_album(album)
                album_data = getconnection.get_collection("Albuns").find_one({'_id': id})
                print("")

                print(" 1 - TItulo do album\n"
                    "2 - Artista\n",
                    "3 - Gênero\n", 
                    "4 - Ano\n", 
                    "5 - Musicas")
                
                aux = int(input("> Digite o valor correspontente do que você deseja alterar: "))


                if album_data:
                    #cria uma instância com a
                    album = Albuns(album_data['album'], album_data['ano'], album_data['artista'], album_data['gênero'])

                    auxiliar.print_info_album(album)
                    print("")


                    if aux == 5:
                        menu = menuMusica()
                        menu.mudar_musica()
                        mudanca = str(input("> Digite a alteração "))
                    
                    else:    
                        mudanca = str(input("> Digite a alteração "))
                        album.editar_album(aux, mudanca)
                        
                else:
                    print("Album não encontrado no banco de dados.")
                    
                editar_mais = input("> Deseja realizar mais alterações? (s/n): ").strip().lower()
                if editar_mais != 's':
                    clear_screen()
                    break
            
            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")


    def apagar_album(self) -> None:
        
        '''
        método de interface para apagar um álbum do banco de dados
        '''
        
        while True:

            try:
        
                print("=" * 30)
                print("{:^30}".format("Apagar Álbum"))
                print("=" * 30) 
                print("")

                titulo = str(input("> Qual o nome do álbum que você deseja apagar: "))
                id = auxiliar.buscar_album(titulo)
                album_data = getconnection.get_collection("Albuns").find_one({'_id': id})
                print("")
                
                if album_data:
                    #cria uma instância com a
                    album = Albuns(album_data['album'], album_data['ano'], album_data['artista'], album_data['gênero'])

                    print("")
                    auxiliar.print_info_album(album)
                    print("")

                    aux = str(input("> Esse é o álbum que você deseja apagar? (s/n) ")).strip().lower()
                    if aux == 's':
                        album.apagar_album()

                apagar_mais = input("> Deseja apagar outro álbum? (s/n): ").strip().lower()
                if apagar_mais != 's':
                    clear_screen()
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")
        

    def render(self):

        '''
        método para renderizar a interface
        '''

        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)


    def next1(self, option) -> None:
        
        '''
        @param option: inteiro responsável por representar a ação desejada do usuário
        metodo next: capaz de seguir o que o usuario deseja realizar
        '''

        clear_screen()  
        if option == 1:
            self.render()
            self.adicionar_album()

        elif option == 2:
            self.render()
            self.editar_album()

        elif option == 3:
            self.render()
            self.apagar_album()

        elif option == 4:
            self.render()
            excel = Excel()
            excel.importar_excel()

        elif option == 5:
            self.next = "Voltar"
    
