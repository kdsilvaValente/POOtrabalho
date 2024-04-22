import pandas as pd 
from run import getconnection  

class Musica:
    
    #crias os atributos das musicas
    def __init__(self, numero, titulo, compositores, produtores, duracao):
        self.numero = numero
        self.titulo = titulo
        self.compositores = compositores
        self.produtores = produtores
        self.duracao = duracao

    #adiciona cada musica ao mongodb
    def adicionar_para_mongodb(self, album_nome, colecao):
        dados_musica = {
            'album': album_nome,
            'numero': self.numero,
            'titulo': self.titulo,
            'compositores': self.compositores,
            'produtores': self.produtores,
            'duracao': self.duracao
        }
        #insere no banco de dados
        colecao.insert_one(dados_musica)

class Album:
    def __init__(self):
        
        #cria conexao com a coleção
        self.colecao = getconnection.get_collection("Albuns")

        #cria um dicionario para albuns
        self.albuns = {}

    #metodos para ler o excel
    def importar_excel(self, caminho_arquivo):
        #armazenar as musicas importadas
        musicas_importadas = set()

        dados_excel = pd.read_excel(caminho_arquivo)

        #leitura da planilha associando a musicas
        for indice, linha in dados_excel.iterrows():
            nome_album = linha['Album']
            artista = linha['Artista']
            genero = linha['Genero']
            ano = linha['Ano']
            musica = Musica(
                indice+1, linha['Título'], linha['Compositores'], 
                linha['Produtores'], str(linha['Duração'])
            )
            
            #verificação de existencia
            if (nome_album, musica.titulo) not in musicas_importadas:
                musicas_importadas.add((nome_album, musica.titulo))
                
                if nome_album not in self.albuns:
                    self.albuns[nome_album] = {'artista': artista, 'genero': genero, 'ano': ano, 'musicas': []}
                
                #adicionar musica a um album
                self.albuns[nome_album]['musicas'].append(musica)

    #adicionando ao mongo db 
    def importar_para_mongodb(self):
        for nome_album, info_album in self.albuns.items():
            #verificação
            if self.colecao.find_one({'album': nome_album}) is None:
                dados_album = {
                    'album': nome_album,
                    'artista': info_album['artista'],
                    'genero': info_album['genero'],
                    'ano': info_album['ano'],
                    'musicas': []
                }
                for musica in info_album['musicas']:
                    # Adiciona cada música ao MongoDB
                    musica.adicionar_para_mongodb(nome_album, self.colecao)
                # Insere o álbum no MongoDB
                self.colecao.insert_one(dados_album)

        print("Todos os álbuns foram importados com sucesso!")

# Criando uma instância de Album
album = Album()

# Importando a planilha para a memória
album.importar_excel(r"C:\Users\gabri\Documents\OMG_SISTEMAS\03_SEMESTRE\POO\ALBUMATIC\POOtrabalho\musicas_planilha.xlsx")

# Importando os dados da planilha para o MongoDB
album.importar_para_mongodb()
