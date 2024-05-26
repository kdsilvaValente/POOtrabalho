from Auxiliares_uteis import Auxiliar
from run import getconnection
import numpy as np
from Albuns import Albuns

class Musica:
    def __init__(self, numero:int, titulo:str, artista:str, album:str, genero:str, 
                compositores:str, produtores:str, duracao:str, albumid) -> None:

        ''''
        construtor de musica.
        
        :param numero: número da faixa no álbum
        :param titulo: título da música
        :param artista: artista ou banda que gravou a música
        :param album: nome do álbum ao qual a música pertence
        :param genero: lista de gêneros musicais 
        :param compositores: lista de compositores 
        :param produtores: lista de produtores
        :param duracao: duração da musica
        :param album_id: id do album na coleção albuns
        
        '''

        self.numero = numero
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = str(genero)
        self.compositores = str(compositores)
        self.produtores = str(produtores)
        self.duracao = duracao
        self.album_id = albumid 

    def adicionar_para_mongodb_Excel(self, colecao):
        auxiliar = Auxiliar()

        ''''
        método que adiciona uma musica da planilha no excel na coleção desejada
        
        :param colecao: nome da coleção que deseja adicionar a faixa
        
        '''

        #separa os compositores e produtores em arrays a partir do ·
        compositores_array = self.compositores.split(" · ")
        produtores_array = self.produtores.split(" · ")
        generos_array = self.genero.split(" · ")
    
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

    def atualizar_no_mongodb(self):

        ''''
        método que atualiza o ID do álbum na musica
        '''

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

    def adicionar_musica(self):

        ''''
        método para adicionar uma música
                
        '''

        auxiliar = Auxiliar()
        album = Albuns()

        colecao_musica = getconnection.get_collection("Musica")

        compositores_array = input("compositores (separados por vírgula): ").split(',')
        produtores_array = input("produtores (separados por vírgula): ").split(',')
        generos_array = input("generos (separados por vírgula): ").split(',')


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

        #insere no banco de dados na coleção musicas e albuns
        if not auxiliar.verificar_existencia_musica(self.titulo, self.album, self.artista):
            colecao_musica.insert_one(dados_musica)  
            Albuns.inserir_musicas_em_albuns(album)

        else:
            print("A música já existe no banco de dados")

    def editar_musica(self, titulo:str, artista:str, campo:int, mudança:str):

        ''''
        método para editar uma musica do banco de dados
        
        :param titulo: nome da musica,
        :param artista: nome do artista,
        :param campo: inteiro relacionado a qual dado da música será alterado
        :param mudança: alteração que será feita
        
        '''

        colecao_musicas = getconnection.get_collection("Musica")
        
        musica = colecao_musicas.find_one({'titulo': titulo}, {'artista': artista})
        if not musica:
            print(f"Musica '{titulo}' não encontrado no banco de dados.")
            return
        
        # relação do inteiro com o que será alterado da musica
        if campo == '1':
            novos_dados = {'titulo': mudança}
        elif campo == '2':
            novos_dados = {'album': mudança}
        elif campo == '3':
            novos_dados = {'artista': mudança}
        elif campo == '4':
            novos_dados = {'genero': mudança}
        elif campo == '5':
            novos_dados = {'compositores': mudança}
        elif campo == '6':
            novos_dados = {'produtores': mudança}
        elif campo == '7':
            novos_dados = {'duracao': mudança}
        else:
            print("Campo inválido. ")
            return
            
        # atualiza a musica na coleção
        colecao_musicas.update_one({'_id': musica['_id']}, {"$set": novos_dados})
        print(f"Musica '{titulo}' atualizada com sucesso.")
    

    def apagar_musica(self):

        '''
        método para apagar uma musica do banco de dados

        '''
        colecao_musicas = getconnection.get_collection("Musica")
        
        musica = colecao_musicas.find_one({'titulo': self.titulo})
        if not musica:
            print(f"Musica '{self.titulo}' não encontrado no banco de dados.")
            return
        
        # deletando do campo com base no títlo
        colecao_musicas.delete_one({'musica': self.titulo})
        print(f"Musica '{self.titulo}' apagada com sucesso.")
    
    @staticmethod
    def exibir_musicas():

        '''
        método estático que exibe todas as musicas do banco de dados
        '''

        colecao = getconnection.get_collection("Musica")
        musicas = colecao.find({}, {"_id": 0, "titulo": 1, "album": 1})

        for musica in musicas:
            print(f"Álbum: {musica['album']}, Música: {musica['titulo']}")