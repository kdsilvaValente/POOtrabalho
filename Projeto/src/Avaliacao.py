from bson.objectid import ObjectId
from run import getconnection


class Avaliacao():
    def __init__(self):
        """
        Inicializa a classe Avaliacao, estabelecendo conexões com as coleções necessárias no banco de dados.
        """
        self.getconnection = getconnection
        self.__musicacollection = self.getconnection.get_collection('Musica')
        self.__usercollection = self.getconnection.get_collection("User")
        self.__avaliacaocollection = self.getconnection.get_collection("Avaliacao")
        self.__comentariocollection = self.getconnection.get_collection("Comentarios")
        self.__albumcollection = self.getconnection.get_collection("Albuns")
        self.sum = None
        self.numUsers = None

    def validar_album(self, idalbum: ObjectId) -> dict:
        """
        Valida a existência de um álbum no banco de dados.

        Args:
            idalbum (ObjectId): ID do álbum a ser validado.

        Returns:
            dict: Documento do álbum se encontrado.

        Raises:
            ValueError: Se o álbum não for encontrado.
        """
        album = self.__albumcollection.find_one({"_id": ObjectId(idalbum)})
        if not album:
            raise ValueError(f"Album não foi encontrado.")
        return album
    
    def validar_musica(self, idmusica: ObjectId) -> dict:
        """
        Valida a existência de uma música no banco de dados.

        Args:
            idmusica (ObjectId): ID da música a ser validada.

        Returns:
            dict: Documento da música se encontrada.

        Raises:
            ValueError: Se a música não for encontrada.
        """
        musica = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        if not musica:
            raise ValueError(f"Música não foi encontrada.")
        return musica

    def validar_usuario(self, idUser: ObjectId) -> dict:
        """
        Valida a existência de um usuário no banco de dados.

        Args:
            idUser (ObjectId): ID do usuário a ser validado.

        Returns:
            dict: Documento do usuário se encontrado.

        Raises:
            ValueError: Se o usuário não for encontrado.
        """
        user = self.__usercollection.find_one({"_id": ObjectId(idUser)})
        if not user:
            raise ValueError("Usuário não foi encontrado.")
        return user
    
    def notaGeral(self):
        if self.numUsers == 0:
            raise ValueError("Número de usuários não pode ser zero.")
        return self.sum / self.numUsers
    
    def darLike(self, idmusica: ObjectId, idUser: ObjectId) -> str:
        """
        Adiciona um like a uma música.

        Args:
            idmusica (ObjectId): ID da música a ser curtida.
            idUser (ObjectId): ID do usuário que está curtindo a música.

        Returns:
            str: Mensagem confirmando a ação.
        """
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))
        
        username = user["name"]
        musicname = music["titulo"]

        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas_curtidas": ObjectId(idmusica)}
        )
        if usuario_curtiu:
            return f"Usuário {username} já curtiu a música {musicname}."

        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$addToSet": {"musicas_curtidas": idmusica}}
        )

        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": 1}}
        )
        
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "musica curtida"
        })

        return f"Usuário {username} deu like na música {musicname}."

    def desfazerLike(self, idmusica: ObjectId, idUser: ObjectId) -> str:
        """
        Remove um like de uma música.

        Args:
            idmusica (ObjectId): ID da música da qual o like será removido.
            idUser (ObjectId): ID do usuário que está removendo o like.

        Returns:
            str: Mensagem confirmando a ação.
        """
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))

        username = user["name"]
        musicname = music["titulo"]

        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas_curtidas": ObjectId(idmusica)}
        )
        if not usuario_curtiu:
            return f"Usuário {username} não curtiu a música {musicname}."

        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$pull": {"musicas_curtidas": idmusica}}
        )

        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": -1}}
        )
        
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "desfazer curtida"
        })

        return f"Usuário {username} desfez like na música {musicname}."

    def darNota(self, idmusica: ObjectId, idUser: ObjectId, nota: int) -> str:
        """
        Avalia uma música com uma nota de 1 a 5 estrelas.

        Args:
            idmusica (ObjectId): ID da música a ser avaliada.
            idUser (ObjectId): ID do usuário que está avaliando a música.
            nota (int): Nota de 1 a 5 estrelas.

        Returns:
            str: Mensagem confirmando a ação.

        Raises:
            ValueError: Se a nota for inválida (menor que 1 ou maior que 5).
        """
        musica = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        idAlbum = musica["album_id"]

        if nota < 1 or nota > 5:
            raise ValueError(f"Nota inválida.")

        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))
        
        username = user["name"]
        musicname = music["titulo"]

        usuario_avaliou = self.__avaliacaocollection.find_one({
            "usuario": ObjectId(idUser), 
            "musica": ObjectId(idmusica), 
            "acao": "dar nota em musica"
        })

        if usuario_avaliou:
            return f"Usuário {username} já avaliou a música {musicname}."

        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"avaliacao geral": nota}}
        )
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"n de avaliacoes": 1}}
        )
        
        msc = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        usu = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        somatorio = msc["avaliacao geral"]
        usuarios = usu["n de avaliacoes"]

        self.sum = somatorio
        self.numUsers = usuarios

        notafinal = self.notaGeral()
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$set": {"avaliacao final": notafinal}}
        )

        album = self.__albumcollection.find_one({"_id": ObjectId(idAlbum)})
        musicas_do_album = album["musicas"]

        somatorio_album = 0
        contador_musicas = 0

        for musics_id in musicas_do_album:
            musica = self.__musicacollection.find_one({"_id": ObjectId(musics_id)})
            if "avaliacao final" not in musica:
                self.__musicacollection.update_one(
                    {"_id": ObjectId(musics_id)},
                    {"$set": {"avaliacao final": 0}}
                )
                musica["avaliacao final"] = 0
            if musica["avaliacao final"] != 0:
                somatorio_album += musica["avaliacao final"]
                contador_musicas += 1
    
        if contador_musicas > 0:
            notaalbum = somatorio_album / contador_musicas
        else:
            notaalbum = 0  

        self.__albumcollection.update_one(
            {"_id": ObjectId(idAlbum)},
            {"$set": {"nota album": notaalbum}}
        )
        
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "dar nota em musica"
        })

        return f"Usuário {username} deu {nota} estrelas na música {musicname}."

    def comentar(self, idmusica: ObjectId, idUser: ObjectId, comentario: str) -> str:
        """
        Adiciona um comentário a uma música.

        Args:
            idmusica (ObjectId): ID da música a ser comentada.
            idUser (ObjectId): ID do usuário que está comentando.
            comentario (str): Texto do comentário.

        Returns:
            str: Mensagem confirmando a ação.

        Raises:
            ValueError: Se o comentário for vazio.
        """
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))

        if not comentario.strip():
            return "O comentário não pode ser vazio."
        
        self.__comentariocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "comentario": comentario.strip()
        })

        username = user["name"]
        musicname = music["titulo"]

        return f"Usuário {username} fez um comentário na música {musicname}."

    def exibirComentarios(self, idmusica: ObjectId) -> list[str]:
        """
        Exibe todos os comentários de uma música.

        Args:
            idmusica (ObjectId): ID da música da qual os comentários serão exibidos.

        Returns:
            list[str]: Lista de comentários formatados como strings.
        """
        comentarios = self.__comentariocollection.find({
            "musica": ObjectId(idmusica),
        })
        
        comentarios_formatados = []
        
        comentarios_count = self.__comentariocollection.count_documents({"musica": ObjectId(idmusica)})
        
        if comentarios_count == 0:
            comentarios_formatados.append("Nenhum comentário disponível.\n")
        else:
            for comentario in comentarios:
                usuario = self.__usercollection.find_one({
                    "_id": ObjectId(comentario["usuario"])
                })
                comentario_formatado = f"{usuario['name']}: {comentario['comentario']}"
                comentarios_formatados.append(comentario_formatado)
            
        return comentarios_formatados

    def favoritarAlbum(self, idalbum: ObjectId, idUser: ObjectId) -> str:
        """
        Favorita um álbum para um usuário.

        Args:
            idalbum (ObjectId): ID do álbum a ser favoritado.
            idUser (ObjectId): ID do usuário que está favoritando o álbum.

        Returns:
            str: Mensagem confirmando a ação.
        """
        alb = self.validar_album(ObjectId(idalbum))
        user = self.validar_usuario(ObjectId(idUser))

        username = user["name"]
        albumname = alb["album"]
        
        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "albuns_favoritados": ObjectId(idalbum)}
        )
        if usuario_curtiu:
            return f"Usuário {username} já curtiu o álbum {albumname}."

        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$addToSet": {"albuns_favoritados": idalbum}}
        )

        self.__albumcollection.update_one(
            {"_id": ObjectId(idalbum)},
            {"$inc": {"favoritados": 1}}
        )
        
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "album": ObjectId(idalbum),
            "acao": "musica curtida"
        })

        return f"Usuário {username} deu like no álbum {albumname}."

    def desfavoritarAlbum(self, idalbum: ObjectId, idUser: ObjectId) -> str:
        """
        Remove a favoritação de um álbum para um usuário.

        Args:
            idalbum (ObjectId): ID do álbum a ser desfavoritado.
            idUser (ObjectId): ID do usuário que está desfavoritando o álbum.

        Returns:
            str: Mensagem confirmando a ação.
        """
        alb = self.validar_album(ObjectId(idalbum))
        user = self.validar_usuario(ObjectId(idUser))
        
        username = user["name"]
        albumname = alb["album"]

        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "albuns_favoritados": ObjectId(idalbum)}
        )
        if not usuario_curtiu:
            return f"Usuário {username} não favoritou o álbum {albumname}."

        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$pull": {"albuns_favoritados": idalbum}}
        )

        self.__albumcollection.update_one(
            {"_id": ObjectId(idalbum)},
            {"$inc": {"likes": -1}}
        )
        
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "album": ObjectId(idalbum),
            "acao": "desfazer curtida"
        })
        

        return f"Usuário {username} desfavoritou o álbum {albumname}."

    def comentarAlbum(self, idAlbum: ObjectId, idUser: ObjectId, comentario: str) -> str:
        """
        Adiciona um comentário a um álbum.

        Args:
            idAlbum (ObjectId): ID do álbum a ser comentado.
            idUser (ObjectId): ID do usuário que está comentando.
            comentario (str): Texto do comentário.

        Returns:
            str: Mensagem confirmando a ação.

        Raises:
            ValueError: Se o comentário for vazio.
        """
        alb = self.validar_album(ObjectId(idAlbum))
        user = self.validar_usuario(ObjectId(idUser))

        if not comentario.strip():
                return "O comentário não pode ser vazio."
        
        self.__comentariocollection.insert_one({
            "usuario": ObjectId(idUser),
            "album": ObjectId(idAlbum),
            "comentario": comentario.strip()
        })

        username = user["name"]
        albumname = alb["album"]

        return f"Usuário {username} fez um comentário no álbum {albumname}."

    def exibirComentariosAlbum(self, idAlbum: ObjectId) -> list[str]:
        """
        Exibe todos os comentários de um álbum.

        Args:
            idAlbum (ObjectId): ID do álbum do qual os comentários serão exibidos.

        Returns:
            list[str]: Lista de comentários formatados como strings.
        """
        comentarios = self.__comentariocollection.find({
            "album": ObjectId(idAlbum),
        })

        comentarios_count = self.__comentariocollection.count_documents({"album": ObjectId(idAlbum)})
        comentarios_formatados = []

        if comentarios_count == 0:
            comentarios_formatados.append("Nenhum comentário disponível.\n")
        else:
            for comentario in comentarios:
                usuario = self.__usercollection.find_one({
                    "_id": ObjectId(comentario["usuario"])
                })
                comentario_formatado = f"{usuario['name']}: {comentario['comentario']}\n"
                comentarios_formatados.append(comentario_formatado)
            
        return comentarios_formatados
