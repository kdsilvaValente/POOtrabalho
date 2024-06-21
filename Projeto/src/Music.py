from Auxiliares_uteis import Auxiliar
from run import getconnection
import numpy as np
from Albuns import *

class Musica:
    def __init__(self, numero:int, titulo:str, artista:str, album:str, genero:str, 
                compositores:str, produtores:str, duracao:str, albumid) -> None:
        """
        Construtor de música.
        
        :param numero: número da faixa no álbum
        :param titulo: título da música
        :param artista: artista ou banda que gravou a música
        :param album: nome do álbum ao qual a música pertence
        :param genero: lista de gêneros musicais 
        :param compositores: lista de compositores 
        :param produtores: lista de produtores
        :param duracao: duração da música
        :param album_id: id do álbum na coleção álbuns
        """
        self.numero = numero
        self.titulo = str(titulo)
        self.artista = str(artista)
        self.album = str(album)
        self.genero = str(genero)
        self.compositores = str(compositores)
        self.produtores = str(produtores)
        self.duracao = duracao
        self.album_id = albumid 
    
    def __str__(self):
        """
        Método padrão para imprimir um objeto música com todas as suas informações de inicialização.
        """
        return (f"Musica(\n"
                f"  Numero: {self.numero}\n"
                f"  Titulo: {self.titulo}\n"
                f"  Artista: {self.artista}\n"
                f"  Album: {self.album}\n"
                f"  Genero: {self.genero}\n"
                f"  Compositores: {self.compositores}\n"
                f"  Produtores: {self.produtores}\n"
                f"  Duracao: {self.duracao}\n"
                f"  Album ID: {self.album_id}\n)")

    def adicionar_para_mongodb_Excel(self, colecao):
        """
        Método que adiciona uma música da planilha no Excel na coleção desejada.
        
        :param colecao: nome da coleção que deseja adicionar a faixa
        """
        auxiliar = Auxiliar()

        # Separa os compositores e produtores em arrays a partir do "·"
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

        # Verifica a existência da música no banco
        if not auxiliar.verificar_existencia_musica(self.titulo, self.titulo, self.artista):
            # Insere a música na coleção especificada
            colecao.insert_one(dados_musica)
        else:
            print("A música já existe no banco de dados")

    def atualizar_no_mongodb(self):
        """
        Método que atualiza o ID do álbum na música.
        """
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")

        # Procura o álbum nas coleções de álbuns e músicas
        album = colecao_albuns.find_one({'album': self.album})
        musica = colecao_musicas.find_one({'album': self.album})
    
        if album and musica:
            # Se o álbum for encontrado em ambas as coleções, atualiza o documento na coleção de músicas
            filtro = {"titulo": self.titulo}
            colecao = getconnection.get_collection("Musica")
            novos_valores = {"$set": {"album_id": album['_id']}}
            colecao.update_one(filtro, novos_valores)
        else:
            # Se não for encontrado apenas imprime a mensagem
            print("Não foi possível atualizar no MongoDB. Álbum não encontrado.")

    def adicionar_musica(self):
        """
        Método para adicionar uma música.
        """
        auxiliar = Auxiliar()

        colecao_musica = getconnection.get_collection("Musica")

        dados_musica = {
            'titulo': self.titulo,
            'album': self.album,
            'album_id': self.album_id,
            'numero': self.numero,
            'artista': self.artista,
            'genero': self.genero.split(','),
            'compositores': self.compositores.split(','),
            'produtores': self.produtores.split(','),
            'duracao': self.duracao
        }

        # Insere no banco de dados na coleção músicas e álbuns
        if not auxiliar.verificar_existencia_musica(self.titulo, self.album, self.artista):
            album = Albuns(self.album, 2004, self.artista, self.genero)
            colecao_musica.insert_one(dados_musica)  
            album.criar_albuns()
            Albuns.inserir_musicas_em_albuns(album)
        else:
            print("A música já existe no banco de dados")

    def editar_musica(self, titulo:str, artista:str, campo:int, mudança:str):
        """
        Método para editar uma música do banco de dados.
        
        :param titulo: nome da música
        :param artista: nome do artista
        :param campo: inteiro relacionado a qual dado da música será alterado
        :param mudança: alteração que será feita
        """
        colecao_musicas = getconnection.get_collection("Musica")
        
        musica = colecao_musicas.find_one({'titulo': titulo}, {'artista': artista})
        if not musica:
            print(f"Musica '{titulo}' não encontrado no banco de dados.")
            return titulo
                
        # Relação do inteiro com o que será alterado da música
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
            print("Campo inválido.")
            return
            
        # Atualiza a música na coleção
        colecao_musicas.update_one({'_id': musica['_id']}, {"$set": novos_dados})
        print(f"Musica '{titulo}' atualizada com sucesso.")

        musica_atualizada = colecao_musicas.find_one({'_id': musica['_id']})
        return musica_atualizada

    def apagar_musica(self):
        """
        Método para apagar uma música do banco de dados.
        """
        colecao_musicas = getconnection.get_collection("Musica")
        
        musica = colecao_musicas.find_one({'titulo': self.titulo})
        if not musica:
            print(f"Musica '{self.titulo}' não encontrado no banco de dados.")
            return
        
        # Deletando do campo com base no título
        colecao_musicas.find_one_and_delete({'titulo': self.titulo})
        print(f"Musica '{self.titulo}' apagada com sucesso.")
