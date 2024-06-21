from run import getconnection
from Search import Search
from bson.objectid import ObjectId
import os
import platform


class Auxiliar:
    def __init__(self):
        pass
    
    def verificar_existencia_musica(self, titulo, album, artista):
        colecao = getconnection.get_collection("Musica")
        #consultar a existencia de uma música dentro do banco de dados
        return bool(colecao.find_one({'titulo': titulo, 'album': album, 'artista': artista}))

    def buscar_musica(self, musica):
            acharMusica = Search("Musica")
            self.musica = musica
            resultados = acharMusica.get_by_type("titulo", musica)
            
            if not resultados:
                print("Nenhuma música encontrada com esse título.")
                return None
            
            if len(resultados) > 1:
                print("Achamos muitos resultados!!")
                for idx, resultado in enumerate(resultados):
                    print(f"{idx + 1}. {resultado['titulo']} - {resultado.get('artista', 'Artista desconhecido')}")
                escolha = int(input("Qual desses bops você quer escolher?")) - 1
                if escolha < 0 or escolha >= len(resultados):
                    print("Escolha inválida.")
                    return None
                idmusica = resultados[escolha]['_id']
            else:
                idmusica = resultados[0]['_id']
            
            return idmusica
    
    def buscar_album(self, album):
            acharAlbum = Search("Albuns")
            self.album = album
            resultados = acharAlbum.get_by_type("album", album)
            
            if not resultados:
                print("Nenhum album encontrado com esse título.")
                return None
            
            if len(resultados) > 1:
                print("Achamos muitos resultados!!")
                for idx, resultado in enumerate(resultados):
                    print(f"{idx + 1}. {resultado['album']} - {resultado.get('artista', 'Artista desconhecido')}")
                escolha = int(input("Qual desses bops você quer escolher?")) - 1
                if escolha < 0 or escolha >= len(resultados):
                    print("Escolha inválida.")
                    return None
                idalbum = resultados[escolha]['_id']
            else:
                idalbum = resultados[0]['_id']
            
            return idalbum
    
    def print_info_musica(self, musica):
        """
        Função para imprimir informações de uma música de forma bonita no terminal.

        Args:
        - musica (Musica): Objeto Musica contendo as informações a serem exibidas.
        """
    
        # Montando o quadro com as informações
        print("=" * 70)
        print("Informações da Música")
        print("=" * 70)
        print("Título:        {}".format(musica.titulo))
        print("Artista:       {}".format(musica.artista))
        print("Número:        {}".format(musica.numero))
        print("Álbum:         {}".format(musica.album))
        print("Gêneros:       {}".format(musica.genero))
        print("Compositores:  {}".format(musica.compositores))
        print("Produtores:    {}".format(musica.produtores))
        print("Duração:       {}".format(musica.duracao))
        print("=" * 70)


    def get_musicas_by_album(self, album_nome):
        # Método para buscar uma música pelo ID no banco de dados
        music_collection = getconnection.get_collection("Musica")    
        return music_collection.find({"album": album_nome})

    
    def print_info_album(self, album_doc):
        """
        Função para imprimir informações de um álbum de forma simples no terminal.

        Args:
        - album_doc (dict): Dicionário contendo as informações do álbum a serem exibidas.
        """
        print("=" * 70)
        print("Informações do Álbum")
        print("=" * 70)
        print("Álbum:         {}".format(album_doc.nome))
        print("Artista:       {}".format(album_doc.artista))
        print("Ano:           {}".format(album_doc.ano))
        print("Gênero:        {}".format(album_doc.genero))
        print("Músicas:")

        musicas = self.get_musicas_by_album(album_doc.nome)
        for musica in musicas:
            print(" - {}: {}".format(musica['numero'], musica['titulo']))

        print("=" * 70)

def limpar_terminal():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def testar_tamanho_vetor(tamanho, escolha)->bool:
    """
    :param tamanho: tamanho do vetor
    :param escolha: número escolhido

    garante que a escolha não ultrapasse o limite do vetor
    """
    if escolha > tamanho:
        print("Escolha um número existente!")
        return False
    else:
        return True
    
def printando_divisão()->None:
    print("-"*40)


def printando_divisão_2()->None:
        print("="*40)

