from Auxiliares_uteis import Auxiliar
from run import getconnection
import numpy as np
from Albuns import Albuns

class Musica:
    def __init__(self, numero, titulo, artista, album, genero, compositores, produtores, duracao, albumid):

        #inicia criando os atributos principais das musicas
        self.numero = numero
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.compositores = str(compositores)
        self.produtores = str(produtores)
        self.duracao = duracao
        self.album_id = albumid 

    #metodo para adicionar os dados da planilha no MongoDB
    def adicionar_para_mongodb_Excel(self, colecao):
        auxiliar = Auxiliar()

        #separa os compositores e produtores em arrays a partir do ·
        compositores_array = self.compositores.split(" · ")
        produtores_array = self.produtores.split(" · ")
        generos_array = self.genero.split(" · ")

    
        #insere os dados das musicas
        dados_musica = {
            'titulo': self.titulo,
            'album': self.album,
            'album_id': self.album_id,
            'numero': self.numero,
            'artista': self.artista,
            'genero': generos_array,
            'compositores': compositores_array,
            'produtores': produtores_array,
            'duracao': self.duracao
        }

        #verifica a existencia da musica no banco
        if not auxiliar.verificar_existencia_musica(self.titulo, self.titulo, self.artista):
            #insere a musica na coleçao especificada 
            colecao.insert_one(dados_musica)
        else:
            print("A música já existe no banco de dados")
    
    #método para atualizar o id do álbum das músicas
    def atualizar_no_mongodb(self):

        #conexão com as coleções de musicas e álbuns
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")

        #procura o álbum nas coleções de álbuns e músicas
        album = colecao_albuns.find_one({'album': self.album})
        musica = colecao_musicas.find_one({'album': self.album})

    
        if album and musica:
            #se o álbum for encontrado em ambas as coleções, atualiza o documento na coleção de músicas
            filtro = {"titulo": self.titulo}
            colecao = getconnection.get_collection("Musica")
            novos_valores = {"$set": {"album_id": album['_id']}}
            colecao.update_one(filtro, novos_valores)
        else:
            #se não for encontrado apenas imprime a mensagem
            print("Não foi possível atualizar no MongoDB. Álbum não encontrado.")

    @staticmethod
    #método para adicionar uma música exclusiva no mongodb
    def adicionar_musica():
        auxiliar = Auxiliar()
        album = Albuns()

        #conexão com as coleções
        colecao_musica = getconnection.get_collection("Musica")
        colecao_albuns = getconnection.get_collection("Albuns")

        #verifica com o usuário se ele deseja adicionar música a um album existente
        resposta = str(input(f'O Album já existe? (S/N)'))
        if resposta == "S":
            todos_albuns = colecao_albuns.find({}, {"_id": 0, "album": 1})
            print("Álbuns no banco de dados:")
            cont = 1
            for album in todos_albuns:
                print(f"{cont}. {album['album']}")
                cont += 1
            
            num = int(input("Digite o numero do álbum correspondente: "))
            todos_albuns.rewind()
            album = None
            for i, album in enumerate(todos_albuns, 1):
                if i == num:
                    album = album['album']
                    break
            if album is None:
                print("Número de álbum inválido!")
                return
            
        #se o album nao existe cria-se um
        else: 
            album = input("Digite o nome do álbum: ")
            artista = input("Digite o nome do artista: ")
            albuns = Albuns()
            albuns.criar_albuns(album, artista)

        #deve-se adicionar as informações da música
        numero = str(input(f'numero:'))
        titulo = str(input(f'titulo:'))
        artista = str(input(f'artista:'))
        duracao = str(input(f'duração:'))

        compositores_array = input("compositores (separados por vírgula): ").split(',')
        produtores_array = input("produtores (separados por vírgula): ").split(',')
        generos_array = input("generos (separados por vírgula): ").split(',')


        #salvando em um dicionario
        dados_musica = {
            'album': album,
            'album_id': 0,
            'numero': numero,
            'titulo': titulo,
            'generos': generos_array,
            'artista': artista,
            'compositores': compositores_array,
            'produtores': produtores_array,
            'duracao': duracao
        }
        #insere no banco de dados na coleção musicas e albuns
        if not auxiliar.verificar_existencia_musica(titulo, album, artista):
            colecao_musica.insert_one(dados_musica)  
            Albuns.inserir_musicas_em_albuns(album)

        else:
            print("A música já existe no banco de dados")

