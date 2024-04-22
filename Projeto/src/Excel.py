import pandas as pd 
from run import getconnection  
from Music import Musica
from Auxiliares_uteis import Auxiliar

class Excel:
    def __init__(self):
        self.musicas_importadas = set() 
        
    #metodos para ler o excel
    def importar_excel(self, caminho_arquivo):
        auxiliar = Auxiliar()
        #armazenar as musicas importadas
        colecao = getconnection.get_collection("Albuns")

        dados_excel = pd.read_excel(caminho_arquivo)

        #leitura da planilha associando a musicas
        for indice, linha in dados_excel.iterrows():
            titulo = linha['Título']
            album = linha['Album']
            compositores = str(linha['Compositores']) if pd.notna(linha['Compositores']) else []
            produtores = str(linha['Produtores']) if pd.notna(linha['Produtores']) else []
            duracao = str(linha['Duração'])
            numero = indice + 1

            if titulo not in self.musicas_importadas:
                # Verificar se a música já existe no banco de dados
                if not auxiliar.verificar_existencia_musica(titulo):
                    musica = Musica(numero, titulo, album, compositores, produtores, duracao)
                    musica.adicionar_para_mongodb(colecao)


                    self.musicas_importadas.add(titulo)

        print("Todas as músicas foram importadas com sucesso!")
        
excel = Excel()
excel.importar_excel(r"C:\Users\gabri\Documents\OMG_SISTEMAS\03_SEMESTRE\POO\ALBUMATIC\POOtrabalho\musicas_planilha.xlsx")