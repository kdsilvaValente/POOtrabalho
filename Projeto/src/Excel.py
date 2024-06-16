import pandas as pd 
from run import getconnection  
from Music import *
from Auxiliares_uteis import *
from Albuns import *

class Excel:
    def __init__(self):
        self.musicas_importadas = set() 
        
    #metodos para ler o excel
    def importar_excel(self):
        auxiliar = Auxiliar()
        
        #armazenar as musicas importadas
        colecao = getconnection.get_collection("Musica")

        dados_excel = pd.read_excel("musicas_planilha.xlsx")


        #leitura da planilha associando a musicas
        for indice, linha in dados_excel.iterrows():
            titulo = linha['Título']
            artista = linha['Artista']
            ano = linha['Ano']
            album = str(linha['Album'])
            genero = str(linha['Genero']) if pd.notna(linha['Genero']) else []
            compositores = str(linha['Compositores']) if pd.notna(linha['Compositores']) else []
            produtores = str(linha['Produtores']) if pd.notna(linha['Produtores']) else []
            duracao = str(linha['Duração'])
            numero = linha['Número']

            
            albuns = Albuns(album, ano, artista, genero)

            #cria os albuns das músicas
            albuns.criar_albuns()

            if titulo not in self.musicas_importadas:
                #verifica se a música já existe no banco de dados
                if not auxiliar.verificar_existencia_musica(titulo, album, artista):
                    musica = Musica(numero, titulo, artista, album, genero, compositores, produtores, duracao, 0)
                    musica.adicionar_para_mongodb_Excel(colecao)
                    
                    #atualiza o id do álbum nas musicas
                    musica.atualizar_no_mongodb()

        #insere as musicas nos albuns já criados
        albuns.inserir_musicas_em_albuns()
        print("Todas as músicas foram importadas com sucesso!")
