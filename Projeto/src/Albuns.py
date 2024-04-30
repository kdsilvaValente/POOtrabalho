from run import getconnection

class Albuns:
    def __init__(self):
        pass

    #funçao que cria albuns
    def criar_albuns(self, nome_album, artista, genero):
        colecao_albuns = getconnection.get_collection("Albuns")
        
        #verifica se o álbum já foi criado
        if colecao_albuns.find_one({'album': nome_album}):
            return
        
        generos_array = genero.split(" · ")

        #cria um documento
        album_doc = {
            'album': nome_album,
            'artista': artista,
            'gênero': generos_array,
            'musicas': []  #não associa nenhuma música a album
            
        }
        #insere o álbum, sem musicas ao documento
        colecao_albuns.insert_one(album_doc)

    #método para adicionar o ID das musicas em Albuns
    def inserir_musicas_em_albuns(self):

        #conexão com as coleções
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")

        #iterar os albuns
        for album in colecao_albuns.find():
            album_id = album['_id']
            album_nome = album['album']

            #localizar todas as músicas que possuam o id do album
            musicas_album = colecao_musicas.find({'album': album_nome}, {'_id': 1})

            #extrae todos os ids das musicas
            ids_musicas = [str(musica['_id']) for musica in musicas_album]

            #atualiza a lista vazia
            colecao_albuns.update_one({'_id': album_id}, {"$set": {'musicas': ids_musicas}})

