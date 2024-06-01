from run import getconnection
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