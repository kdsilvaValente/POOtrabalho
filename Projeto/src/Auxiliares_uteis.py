from run import getconnection
<<<<<<< HEAD
import os
=======
from bson.objectid import ObjectId
>>>>>>> main

class Auxiliar:
    def __init__(self):
        pass
    
    def verificar_existencia_musica(self, titulo, album, artista):
        colecao = getconnection.get_collection("Musica")
        #consultar a existencia de uma música dentro do banco de dados
        return bool(colecao.find_one({'titulo': titulo, 'album': album, 'artista': artista}))

class Validador:
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def validar_musica(self, idmusica):
        musicacollection = self.__db_connection.get_collection("Musica")
        musica = musicacollection.find_one({"_id": ObjectId(idmusica)})
        if not musica:
            raise ValueError(f"Música não foi encontrada.")
        return musica

    def validar_usuario(self, idUser):
        usercollection = self.__db_connection.get_collection("User")
        user = usercollection.find_one({"_id": ObjectId(idUser)})
        if not user:
            raise ValueError("Usuário não foi encontrado.")
        return user




class calcMedia():
    def __init__(self, sum, numUsers):
        self.sum = sum
        self.numUsers = numUsers

    def notaGeral(self):
        if self.numUsers == 0:
            raise ValueError("Número de usuários não pode ser zero.")
        return self.sum / self.numUsers
<<<<<<< HEAD


def limpar_terminal():
    if os.name == 'posix':  # Verifica se é um sistema Unix
        os.system('clear')  # Limpa o terminal no Unix
    elif os.name == 'nt':  # Verifica se é Windows
        os.system('cls')    # Limpa o terminal no Windows
=======
>>>>>>> main
