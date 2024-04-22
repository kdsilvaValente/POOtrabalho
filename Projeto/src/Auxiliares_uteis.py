from run import getconnection

class Auxiliar:
    def __init__(self):
        pass
    
    def verificar_existencia_musica(self, titulo):
        colecao = getconnection.get_collection("Albuns")
        # Consultar o banco de dados para verificar se a música já existe
        return bool(colecao.find_one({'titulo': titulo}))