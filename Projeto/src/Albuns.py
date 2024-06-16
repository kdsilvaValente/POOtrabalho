from run import getconnection


class Albuns:
    def __init__(self, nome:str, ano:int, artista:str, genero:str) -> None:
        
        ''''
        construtor de albuns
        
        :param nome: nome do álbum
        :param ano: ano de lançamento do álbum
        :param artista: artista ou banda que gravou o álbum
        :param genero: lista de gêneros musicais do album
        
        '''
        
        self.nome = nome
        self.ano = ano
        self.artista = artista
        self.genero = genero

    def criar_albuns(self):

        '''
        metodo que cria albuns sem musicas associadas
        '''

        colecao_albuns = getconnection.get_collection("Albuns")
        
        #verifica se o álbum já foi criado
        if colecao_albuns.find_one({'album': self.nome}):
            return self.nome
        
        album_doc = {
            'album': self.nome,
            'artista': self.artista,
            'ano': self.ano,
            'gênero': self.genero,
            'musicas': [] #não associa nenhuma música a album
            
        }
        #insere o álbum, sem musicas ao documento
        colecao_albuns.insert_one(album_doc)

    def inserir_musicas_em_albuns(self):

        '''
        metodo que insere musicas a um álbum já criado
        '''

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

    def editar_album(self, campo:int, mudanca:str):

        '''
        metodo que edita um album no banco de dados
    
        :param campo: inteiro correspondente a o que será alterado
        :param mudanca: valor da alteração que será feita

        '''
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")
        
        album = colecao_albuns.find_one({'album': self.nome})
        if not album:
            print(f"Álbum '{self.nome}' não encontrado no banco de dados.")
            return
        
        # relação do inteiro com o que será alterado no álbum
        if campo == 1:
            novos_dados = {'album': mudanca}
        elif campo == 2:
            novos_dados = {'ano': int(mudanca)}
        elif campo == 3:
            novos_dados = {'artista': mudanca}
        else:
            print("Campo inválido.")
            return
            
        # atualiza o álbum
        colecao_albuns.update_one({'_id': album['_id']}, {"$set": novos_dados})
        print(f"Álbum '{self.nome}' atualizado com sucesso.")

        novos_dados_musica = novos_dados
        #atualiza as musicas associadas ao álbum
        colecao_musicas.update_many({'album': self.nome}, {"$set": novos_dados_musica})
        print(f"Músicas do álbum '{self.nome}' também foram atualizadas com sucesso.")

    
    def apagar_album(self):

        '''
        metodo que apaga um album do banco de dados
        '''
        colecao_albuns = getconnection.get_collection("Albuns")
            
        # Verifica se o álbum existe
        if not colecao_albuns.find_one({'album': self.nome}):
            print(f"Álbum '{self.nome}' não encontrado no banco de dados.")
            return
            
        #apaga o álbum
        colecao_albuns.delete_one({'album': self.nome})
        print(f"Álbum '{self.nome}' apagado com sucesso.")
    
    