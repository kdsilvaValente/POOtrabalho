from bson.objectid import ObjectId
from run import getconnection

class Avaliacao():
    def __init__(self, db_connection) -> None:
        self.__colecaoalbum = "Musica"
        self.__colecaouser = "User"
        self.__colecaoavaliacao = "Avaliacao"
        self.__db_connection = db_connection

    # função que favorita uma musica 
    def darLike(self, idmusica, idUser):
        # adicionando as coleções 
        musicacollection = self.__db_connection.get_collection(self.__colecaoalbum)
        usercollection = self.__db_connection.get_collection(self.__colecaouser)
        avaliacaocollection = self.__db_connection.get_collection(self.__colecaoavaliacao)
        
        # acha a musica ou retorna se ela nao for encontrada
        musica = musicacollection.find_one({"_id": ObjectId(idmusica)})
        if not musica:
            raise ValueError(f"Musica não foi encontrada.")
        
        # confere se o user existe
        user = usercollection.find_one({"_id": ObjectId(idUser)})
        if not user:
            raise ValueError("Usuário não foi encontrado.")
        
        # verificar se o user ja deu like nessa musica
        usuario_curtiu = usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas curtidas": ObjectId(idmusica)}
        )
        if usuario_curtiu:
            return f"Usuário {idUser} já curtiu a música {idmusica}."

        # adicionar o like na coleção de usuários
        usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$addToSet": {"musicas curtidas": idmusica}}
        )

        # adicionar o like na coleção de músicas
        musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": 1}}  # Incrementar o contador de likes
        )
        
        # registrar like em avaliação
        avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "musica curtida"
        })

        return f"Usuário {idUser} deu like na música {idmusica}."

    # função que desfaz um like
    def desfazerLike(self, idmusica, idUser):
        # adicionando as coleções 
        musicacollection = self.__db_connection.get_collection(self.__colecaoalbum)
        usercollection = self.__db_connection.get_collection(self.__colecaouser)
        avaliacaocollection = self.__db_connection.get_collection(self.__colecaoavaliacao)
        
        # acha a musica ou retorna se ela nao for encontrada
        musica = musicacollection.find_one({"_id": ObjectId(idmusica)})
        if not musica:
            raise ValueError(f"Musica não foi encontrada.")
        
        # confere se o user existe
        user = usercollection.find_one({"_id": ObjectId(idUser)})
        if not user:
            raise ValueError("Usuário não foi encontrado.")
        
        # verificar se o user deu like nessa musica
        usuario_curtiu = usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas curtidas": ObjectId(idmusica)}
        )
        if not usuario_curtiu:
            return f"Usuário {idUser} não curtiu a música {idmusica}."

        # tirar o like na coleção de usuários
        usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$pull": {"musicas curtidas": idmusica}}
        )

        # remover o like da coleção de músicas
        musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": -1}}  # Diminui o contador de likes
        )
        
        # registrar deslike em avaliação
        avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "desfazer curtida"
        })

        return f"Usuário {idUser} desfez like na música {idmusica}."


