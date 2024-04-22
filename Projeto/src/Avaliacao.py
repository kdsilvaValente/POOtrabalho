from bson.objectid import ObjectId

class Avaliacao():
    def __init__(self, db_connection) -> None:
        self.__colecaoalbum = "Albuns"
        self.__colecaouser = "User"
        self.__db_connection = db_connection

    def darLike(self, idAlbum, idUser): #por enquanto n vai ter como eu colocar musica, adiciona album favorito a array do usuario
        albumcollection = self.__db_connection.get_collection(self.__colecaoalbum)
        usercollection = self.__db_connection.get_collection(self.__colecaouser)
        
        album = albumcollection.find_one(
            {"_id": ObjectId(idAlbum)},
            { "_id": 0 },
            {"Artista": 0}
        )
        print("ACHEI O ALBUM")
        if not album:
            raise ValueError(f"Álbum com ID {idAlbum} não foi encontrado.")
        
        response = []
        for elem in album: response.append(elem)
        print(response)
        print("_______________________")

        favoritar = usercollection.uptade_one(
            { "_id": idUser }, 
            {"$addToSet": {"albunsFavoritados": response}} # Campo de edição)
        )
        print(favoritar.modified_count) #printa quantos objetos foram modificafos



