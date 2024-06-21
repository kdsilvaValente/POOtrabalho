from run import getconnection  # Importando a função getconnection do módulo run

class Albuns:
    def __init__(self, nome: str, ano: int, artista: str, genero: str) -> None:
        '''
        Construtor da classe Albuns
        
        :param nome: Nome do álbum
        :param ano: Ano de lançamento do álbum
        :param artista: Artista ou banda que gravou o álbum
        :param genero: Gênero musical do álbum
        '''
        self.nome = nome
        self.ano = ano
        self.artista = artista
        self.genero = genero

    def criar_albuns(self):
        '''
        Método que cria álbuns sem músicas associadas
        '''
        colecao_albuns = getconnection.get_collection("Albuns")
        
        # Verifica se o álbum já existe no banco de dados
        if colecao_albuns.find_one({'album': self.nome}):
            # Retorna o nome do álbum se já existir
            return self.nome
        
        album_doc = {
            'album': self.nome,
            'artista': self.artista,
            'ano': self.ano,
            'gênero': self.genero,
            'musicas': []  # Não associa nenhuma música ao álbum inicialmente
        }
        # Insere o documento do álbum na coleção de álbuns
        colecao_albuns.insert_one(album_doc)

    def inserir_musicas_em_albuns(self):
        '''
        Método que insere músicas a um álbum já criado
        '''
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")

        # Itera através dos álbuns
        for album in colecao_albuns.find():
            album_id = album['_id']
            album_nome = album['album']

            # Localiza todas as músicas associadas ao álbum pelo nome
            musicas_album = colecao_musicas.find({'album': album_nome}, {'_id': 1})

            # Extrai todos os IDs das músicas encontradas
            ids_musicas = [str(musica['_id']) for musica in musicas_album]

            # Atualiza a lista de IDs de músicas no documento do álbum
            colecao_albuns.update_one({'_id': album_id}, {"$set": {'musicas': ids_musicas}})

    def editar_album(self, campo: int, mudanca: str):
        '''
        Método que edita informações de um álbum no banco de dados
        
        :param campo: Número correspondente ao campo a ser alterado (1 - nome, 2 - ano, 3 - artista)
        :param mudanca: Novo valor da alteração a ser feita
        '''
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")
        
        album = colecao_albuns.find_one({'album': self.nome})
        if not album:
            print(f"Álbum '{self.nome}' não encontrado no banco de dados.")
            return
        
        # Determina qual campo do álbum será alterado com base no valor de campo
        if campo == 1:
            novos_dados = {'album': mudanca}
        elif campo == 2:
            novos_dados = {'ano': int(mudanca)}
        elif campo == 3:
            novos_dados = {'artista': mudanca}
        else:
            print("Campo inválido.")
            return
        
        # Atualiza as informações do álbum com os novos dados
        colecao_albuns.update_one({'_id': album['_id']}, {"$set": novos_dados})
        print(f"Álbum '{self.nome}' atualizado com sucesso.")

        # Atualiza também as informações das músicas associadas ao álbum
        colecao_musicas.update_many({'album': self.nome}, {"$set": novos_dados})
        print(f"Músicas do álbum '{self.nome}' também foram atualizadas com sucesso.")

    def apagar_album(self):
        '''
        Método que apaga um álbum do banco de dados
        '''
        colecao_albuns = getconnection.get_collection("Albuns")
        colecao_musicas = getconnection.get_collection("Musica")
        
        if not colecao_albuns.find_one({'album': self.nome}):
            print(f"Álbum '{self.nome}' não encontrado no banco de dados.")
            return
        # Remove o álbum do banco de dados
        # colecao_albuns.delete_one({'album': self.nome})

