from Auxiliares_uteis import Auxiliar

class Musica:

    #crias os atributos das musicas
    def __init__(self, numero, titulo, album, compositores, produtores, duracao):
        self.numero = numero
        self.titulo = titulo
        self.album = album
        self.compositores = str(compositores)
        self.produtores = str(produtores)
        self.duracao = duracao

    def get_album(self):
        return self.album_nome

    def get_numero(self):
        return self.numero
    
    def get_titulo(self):
        return self.titulo

    def get_compositores(self):
        return self.compositores

    def get_produtores(self):
        return self.produtores
    
    def get_duracao(self):
        return self.duracao

    def adicionar_para_mongodb(self, colecao):
        auxiliar = Auxiliar()
        compositores_array = self.compositores.split(" · ")
        produtores_array = self.produtores.split(" · ")

        dados_musica = {
            'album': self.album,
            'numero': self.numero,
            'titulo': self.titulo,
            'compositores': compositores_array,
            'produtores': produtores_array,
            'duracao': self.duracao
        }
        #insere no banco de dados
        if not auxiliar.verificar_existencia_musica(self.titulo):
            colecao.insert_one(dados_musica)
        else:
            print("Já adicionada")
