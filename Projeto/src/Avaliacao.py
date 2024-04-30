from bson.objectid import ObjectId

class Avaliacao():
    def __init__(self, db_connection) -> None:
        self.__colecaoalbum = "Musica"
        self.__colecaouser = "User"
        self.__colecaoavaliacao = "Avaliacao"
        self.__db_connection = db_connection

    def darLike(self, idmusica, idUser): #por enquanto n vai ter como eu colocar musica, adiciona album favorito a array do usuario
        musicacollection = self.__db_connection.get_collection(self.__colecaoalbum)
        usercollection = self.__db_connection.get_collection(self.__colecaouser)
        avaliacaocollecion = self.__db_connection.get_collection(self.__colecaoavaliacao)
        
        musica = musicacollection.find_one(
            {"_id": ObjectId(idmusica)},
            {
            "_id": 0 ,
            "album": 0,
            "compositores": 0,
            "produtores": 0,
            "duracao": 0
            }
        )

        print("ACHEI A MUSICA")
        if not musica:
            raise ValueError(f"Álbum com ID {idmusica} não foi encontrado.")
        
        musicaFav = []
        for elem in musicaFav: musicaFav.append(elem)
        print(musicaFav)
        print("_______________________")

        favoritar = usercollection.update_one(
            { "_id": ObjectId(idUser) }, 
            {"$addToSet": {"albunsFavoritados": musicaFav}} # Campo de edição)
        )
        print(favoritar.modified_count) #printa quantos objetos foram modificafos
        
        avaliacaocollecion.insert_one({"Musica Favoritada": ObjectId(idmusica), "usuario": ObjectId(idUser)}) #inserir no banco avaliacao o registro dessa ação
    