from bson.objectid import ObjectId
from run import getconnection
from Auxiliares_uteis import calcMedia 


class Avaliacao():
    def __init__(self):
        self.__musicacollection = getconnection.get_collection('Musica')
        self.__usercollection = getconnection.get_collection("User")
        self.__avaliacaocollection = getconnection.get_collection("Avaliacao")
        self.__comentariocollection = getconnection.get_collection("Comentarios")
        self.__albumcollection = getconnection.get_collection("Albuns")
        

    def validar_album(self, idalbum: ObjectId):
        a = self.__musicacollection
        print(a)

        album = self.__albumcollection.find_one({"_id": ObjectId(idalbum)})
        if not album:
            raise ValueError(f"Album não foi encontrado.")
        return album
    
    def validar_musica(self, idmusica: ObjectId):
        musica = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        if not musica:
            raise ValueError(f"Música não foi encontrada.")
        return musica

    def validar_usuario(self, idUser:ObjectId):
        user = self.__usercollection.find_one({"_id": ObjectId(idUser)})
        if not user:
            raise ValueError("Usuário não foi encontrado.")
        return user
    
    # função que favorita uma musica 
    def darLike(self, idmusica, idUser):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))
        
        # verificar se o user ja deu like nessa musica
        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas curtidas": ObjectId(idmusica)}
        )
        if usuario_curtiu:
            return f"Usuário {idUser} já curtiu a música {idmusica}."

        # adicionar o like na coleção de usuários
        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$addToSet": {"musicas curtidas": idmusica}}
        )

        # adicionar o like na coleção de músicas
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": 1}}  # Incrementar o contador de likes
        )
        
        # registrar like em avaliação
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "musica curtida"
        })

        username = user["name"]
        musicname = music["titulo"]

        return f"Usuário {username} deu like na música {musicname}."

    # função que desfaz um like
    def desfazerLike(self, idmusica, idUser):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))

        # verificar se o user deu like nessa musica
        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "musicas curtidas": ObjectId(idmusica)}
        )
        if not usuario_curtiu:
            return f"Usuário {idUser} não curtiu a música {idmusica}."

        # tirar o like na coleção de usuários
        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$pull": {"musicas curtidas": idmusica}}
        )

        # remover o like da coleção de músicas
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"likes": -1}}  # Diminui o contador de likes
        )
        
        # registrar deslike em avaliação
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "desfazer curtida"
        })

        username = user["name"]
        musicname = music["titulo"]

        return f"Usuário {username} desfez like na música {musicname}."

# função de avaliação na música (0 a 5 estrelas) e atualiza avaliacao final(NAO ESTA PRONTA)
    def darNota(self, idmusica:ObjectId, idUser:ObjectId, nota:int):
    
        #pegando o id do album pela musica 
        musica = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        idAlbum = musica["album_id"]

        # nota menor que 1 ou maior que 5
        if self.nota < 1 or self.nota > 5:
            raise ValueError(f"Nota inválida.")

        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))
        
        # verificar se o user deu nota nessa musica
        usuario_avaliou = self.__avaliacaocollection.find_one({
            "usuario": ObjectId(idUser), 
            "musica": ObjectId(idmusica), 
            "acao": "dar nota em musica"
        })

        if usuario_avaliou:
            return f"Usuário {idUser} já avaliou a música {idmusica}."

        # dar nota de musica
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"avaliacao geral": nota}}  # avalia uma música
        )
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$inc": {"n de avaliacoes": 1}}  # conta quantas pessoas fizeram uma avaliacao
        )
        
        #calcular nota da avaliação geral
        #pegar valores
        msc = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        usu = self.__musicacollection.find_one({"_id": ObjectId(idmusica)})
        somatorio = msc["avaliacao geral"]
        usuarios = usu["n de avaliacoes"]

        #instancir classe media e calcular media
        media = calcMedia(somatorio, usuarios)
        notafinal = media.notaGeral()
        self.__musicacollection.update_one(
            {"_id": ObjectId(idmusica)},
            {"$set": {"avaliacao final": notafinal}}  # avalia uma música
        )

        album = self.__albumcollection.find_one({"_id": ObjectId(idAlbum)})
        musicas_do_album = album["musicas"]

        somatorio_album = 0  # Inicializa o somatório das notas do álbum
        contador_musicas = 0  # Contador de músicas com avaliação final

        for musics_id in musicas_do_album:
            musica = self.__musicacollection.find_one({"_id": ObjectId(musics_id)})
            if "avaliacao final" not in musica:
                # Adiciona campo avaliacao final com valor 0
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
        
        # registrar avaliação de música
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "acao": "dar nota em musica"
        })

        username = user["name"]
        musicname = music["titulo"]

        return f"Usuário {username} deu {nota} estrelas na música {musicname}."

    def comentar(self, idmusica, idUser, comentario):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        music = self.validar_musica(ObjectId(idmusica))
        user = self.validar_usuario(ObjectId(idUser))

        #teste comentario vazio
        if not comentario.strip():
                return "O comentário não pode ser vazio."
        
        #adicionar comentario e relacionar com a musica e o usuario 
        self.__comentariocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idmusica),
            "comentario": comentario.strip()
        })

        username = user["name"]
        musicname = music["titulo"]

        return f"Usuário {username} fez um comentário na música {musicname}."
    
    # função que favorita um album 
    def favoritarAlbum(self, idalbum, idUser):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        alb = self.validar_album(ObjectId(idalbum))
        user = self.validar_usuario(ObjectId(idUser))
        
        # verificar se o user ja deu like nessa musica
        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "albuns favoritados": ObjectId(idalbum)}
        )
        if usuario_curtiu:
            return f"Usuário {idUser} já curtiu esse álbum {idalbum}."

        # adicionar o like na coleção de usuários
        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$addToSet": {"albuns favoritados": idalbum}}
        )

        # adicionar o like na coleção de músicas
        self.__albumcollection.update_one(
            {"_id": ObjectId(idalbum)},
            {"$inc": {"favoritados": 1}}  # Incrementar o contador de likes
        )
        
        # registrar like em avaliação
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "album": ObjectId(idalbum),
            "acao": "musica curtida"
        })

        username = user["name"]
        albumname = alb["album"]

        return f"Usuário {username} deu like no album {albumname}."

    # função que desfaz um like
    def desfavoritarAlbum(self, idalbum:ObjectId, idUser:ObjectId):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        alb = self.validar_album(ObjectId(idalbum))
        user = self.validar_usuario(ObjectId(idUser))
        
        # verificar se o user deu like nessa musica
        usuario_curtiu = self.__usercollection.find_one(
            {"_id": ObjectId(idUser), "albuns favoritados": ObjectId(idalbum)}
        )
        if not usuario_curtiu:
            return f"Usuário {idUser} não favoritou esse album {idalbum}."

        # tirar o like na coleção de usuários
        self.__usercollection.update_one(
            {"_id": ObjectId(idUser)},
            {"$pull": {"musicas curtidas": idalbum}}
        )

        # remover o like da coleção de músicas
        self.__albumcollection.update_one(
            {"_id": ObjectId(idalbum)},
            {"$inc": {"likes": -1}}  # Diminui o contador de likes
        )
        
        # registrar deslike em avaliação
        self.__avaliacaocollection.insert_one({
            "usuario": ObjectId(idUser),
            "album": ObjectId(idalbum),
            "acao": "desfazer curtida"
        })
        
        username = user["name"]
        albumname = alb["album"]

        return f"Usuário {username} desfavoritou o album {albumname}."
    
    def comentarAlbum(self, idAlbum, idUser, comentario):
        
        # acha a musica ou retorna se ela nao for encontrada e confere se usuario existe
        alb = self.validar_album(ObjectId(idAlbum))
        user = self.validar_usuario(ObjectId(idUser))

        #teste comentario vazio
        if not comentario.strip():
                return "O comentário não pode ser vazio."
        
        #adicionar comentario e relacionar com a musica e o usuario 
        self.__comentariocollection.insert_one({
            "usuario": ObjectId(idUser),
            "musica": ObjectId(idAlbum),
            "comentario": comentario.strip()
        })

        username = user["name"]
        albumname = alb["album"]

        return f"Usuário {username} fez um comentário na música {albumname}."
