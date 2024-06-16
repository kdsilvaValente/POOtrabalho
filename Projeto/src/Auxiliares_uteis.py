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

class calcMedia():
    def __init__(self, sum, numUsers):
        self.sum = sum
        self.numUsers = numUsers

    def notaGeral(self):
        if self.numUsers == 0:
            raise ValueError("Número de usuários não pode ser zero.")
        return self.sum / self.numUsers


def limpar_terminal():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")