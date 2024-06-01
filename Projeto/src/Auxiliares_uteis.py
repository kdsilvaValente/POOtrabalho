from run import getconnection
from bson.objectid import ObjectId

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

class calcMedia():
    def __init__(self, sum, numUsers):
        self.sum = sum
        self.numUsers = numUsers

    def notaGeral(self):
        if self.numUsers == 0:
            raise ValueError("Número de usuários não pode ser zero.")
        return self.sum / self.numUsers