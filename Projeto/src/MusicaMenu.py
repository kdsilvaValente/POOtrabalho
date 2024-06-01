from AbstractMenu import *
from Music import *
from Excel import * 

class menuMusica(Menu):
    def __init__(self):
        self.title = "Menu Musica :p"
        self.options = [
            "1 - Adicionar uma música",
            "2 - Editar música",
            "3 - Apagar música",
            "4 - Exibir musicas do banco",
            "5 - Ler Excel novamente"
        ]

    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)

        print("\n>> Digite sua opção")

    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        if option == 1:
            print("Adicione uma musica")
            
            titulo = str(input("Titulo: "))
            album = str(input("Album: "))
            numero = str(input("Numero: "))
            artista = str(input("Artista: "))
            generos_array = str(input("Genero: "))
            compositores_array = str(input("Compositores: "))
            produtores_array = str(input("Produtores: "))
            duracao = str(input("Duração: "))

            musica = Musica(numero, titulo, artista, album, generos_array, compositores_array, produtores_array, duracao, 0)
            musica.adicionar_musica()

        elif option == 2:
            print("Editar musica")
            titulo = str(input("Qual o nome da musica que você deseja alterar: "))
            artista = str(input("Qual o nome do artista da musica que você deseja alterar: "))

            musica_data = getconnection.get_collection("Musica").find_one({'titulo': titulo, 'artista': artista})
            print(musica_data)


            print("1 - Título\n 2 - Album\n 3 - Artista\n 4 - Gênero\n 5 - Compositores\n 6 - Produtores\n 7 - Duração")
            aux = str(input("Digite o valor correspontente do que você deseja alterar: "))
            mudanca = str(input("Digite a alteração "))


            if musica_data:
                # Cria uma instância de Musica com os dados recuperados do banco de dados
                musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                        musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                        musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])

                musica.editar_musica(titulo, artista, aux, mudanca)
                
            else:
                print("Música não encontrada no banco de dados.")

        elif option == 3:
            print("Apagar musica")
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

        elif option == 4:
            print("Exibindo todas as musicas do banco de dados")
            Musica.exibir_musicas()
        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
    
menu = menuMusica()
menu.render()
menu.next(2)