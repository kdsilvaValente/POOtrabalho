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

        self.title = "Menu Albuns :p"
        self.options = [
            "1 - Adicionar um album",
            "2 - Editar album",
            "3 - Apagar album",
            "4 - Exibir albuns do banco",
            "5 - Ler Excel novamente"
        ]


    def adicionar_album(self) -> None:
        
        '''
        método de interface para adicionar um álbum ao banco de dados 
        '''
        
        while True:

            clear_screen()
            print("-------------------------------")
            print("Digite as informações do album que deseja adicionar")
            
            album_titulo = str(input("Nome: "))
            artista = str(input("Artista: "))
            generos_array = str(input("generos (separados por vírgula): ")).split(',')
            ano = int(input("Ano:"))

            album = Albuns(album_titulo, ano, artista, generos_array)
            album.criar_albuns()

            while True:
                
                print("Digite as musicas do álbum:")
                titulo = str(input("Titulo: "))
                numero = input("Numero: ")
                compositores_array = input("compositores (separados por vírgula): ").split(',')
                produtores_array = input("produtores (separados por vírgula): ").split(',')
                duracao = str(input("Duração: "))

                musica = Musica(numero, titulo, artista, album, generos_array, compositores_array, produtores_array, duracao, 0)
                musica.adicionar_musica()
            
                adicionar_mais = input("Deseja adicionar outra música? (s/n): ").strip().lower()
                if adicionar_mais != 's':
                    album.inserir_musicas_em_albuns()
                    break
            
            adicionar_mais_albuns = input("Deseja adicionar outro album? (s/n): ").strip().lower()
            if adicionar_mais_albuns != 's':
                break
    

    def editar_album(self) -> None:

        '''
        método de interface para editar informações de um álbum no banco de dados
        '''

        while True:

            clear_screen()
            print('aaaaaaaaaaaaaaaaaaaa')
            print("Editar album")
            album = str(input("Qual o nome do álbum que você deseja alterar: "))
            id = auxiliar.buscar_album(album)
            album_data = getconnection.get_collection("Albuns").find_one({'_id': id})
            print(album_data)

            print(" 1 - TItulo do album\n 2 - Artista\n 3 - Gênero\n 4 - Ano \n 5 - Musicas")
            aux = int(input("Digite o valor correspontente do que você deseja alterar: "))


            if album_data:
                #cria uma instância com a
                album = Albuns(album_data['album'], album_data['ano'], album_data['artista'], album_data['gênero'])

                if aux == 5:
                    menu = menuMusica()
                    menu.mudar_musica()
                    mudanca = str(input("Digite a alteração "))
                
                else:    
                    mudanca = str(input("Digite a alteração "))
                    album.editar_album(aux, mudanca)
                    
            else:
                print("Album não encontrado no banco de dados.")
                
            editar_mais = input("Deseja realizar mais alterações? (s/n): ").strip().lower()
            if editar_mais != 's':
                break


    def apagar_album(self) -> None:
        
        '''
        método de interface para apagar um álbum do banco de dados
        '''
        
        while True:
        
            print("Apagar album")
            titulo = str(input("Qual o nome da musica que você deseja apagar: "))
            artista = str(input("Qual o nome do artista da musica que você deseja apagar: "))

            musica_data = getconnection.get_collection("Musica").find_one({'titulo': titulo, 'artista': artista})

            if musica_data:
                #cria musica
                musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                        musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                        musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])
                print(musica)
                aux = str(input("Essa é a musica que você deseja apagar? (S/N) "))
                if aux == 'S':
                    musica.apagar_musica()
                elif aux == 'N':
                    pass   
            
            apagar_mais = input("Deseja adicionar outra música? (s/n): ").strip().lower()
            if apagar_mais != 's':
                break
        

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

        print("\n>> Digite sua opção")


    def next(self, option) -> None:
        
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
        
        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
    
