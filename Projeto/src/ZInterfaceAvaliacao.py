from Avaliacao import *
from AbstractMenu import *
from Search import *
from run import getconnection
            
mainmenu = MainMenu()

class AvaliacaoInterface(Menu):
    def __init__(self, idUser):
        self.user = idUser
        self.title = "Vamos avaliar!"
        self.options = [
            "1 - Favoritar uma musica!!! To apaixonado nessa aqui ó:",
            "2 - Remover like, não gosto mais dela (emoji nojo)",
            "3 - Me sentindo crítico, quero dar nota pra essa música",
            "4 - Tenho mt a dizer!!!! Quero comentar uma música ou um álbum",
        ]

    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)
    
    def finalAcao(self):
        print("O que você deseja fazer agora?")
        print("1 - Voltar ao menu principal")
        print("2 - Continuar avaliando")
        next_option = input("Escolha uma opção: ")

        if next_option == '1':
            mainmenu.render()
            option = int(input("Escolha uma opção: "))
            mainmenu.next(option)
        elif next_option == '2':
            self.render()
            option = int(input("Escolha uma opção: "))
            self.next(option)
        else:
            print("Opção inválida.")
            self.finalAcao()

    def buscar_musica(self, musica):
        acharMusica = Search("Musica")
        self.musica = musica
        resultados = acharMusica.get_by_type("titulo", musica)
        
        if not resultados:
            print("Nenhuma música encontrada com esse título.")
            return None
        
        if len(resultados) > 1:
            print("Achamos muitos resultados!!")
            for idx, resultado in enumerate(resultados):
                print(f"{idx + 1}. {resultado['titulo']} - {resultado.get('artista', 'Artista desconhecido')}")
            escolha = int(input("Qual desses bops você quer escolher?")) - 1
            if escolha < 0 or escolha >= len(resultados):
                print("Escolha inválida.")
                return None
            idmusica = resultados[escolha]['_id']
        else:
            idmusica = resultados[0]['_id']
        
        return idmusica
    
    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        avaliar = Avaliacao(getconnection)
        
        if option == 1:
            musica = input("Qual linda canção você vai favoritar?")
            idmusica = self.buscar_musica(musica)
            
            if idmusica is None:
                print("Música não encontrada!! Digite novamente")
                self.next(1)
                return
            
            like = avaliar.darLike(idmusica, self.user)
            print(like)
            self.finalAcao()

        elif option == 2:
            musica = input("Vai desfazer o like de qual música? :(")
            idmusica = self.buscar_musica(musica)
            
            if idmusica is None:
                print("Música não encontrada!! Digite novamente")
                self.next(2)
            
            deslike = avaliar.desfazerLike(idmusica, self.user)
            print(deslike)
            self.finalAcao()

        elif option == 3:
            musica = input("Então tá bem!! Qual música você quer dar nota?")
            idmusica = self.buscar_musica(musica)
            
            if idmusica is None:
                print("Música não encontrada!! Digite novamente")
                self.next(3)
            
            nota = input("De uma a 5 estrelas, qual nota você quer dar pra essa música?")
            darnota = avaliar.darNota(idmusica, self.user, nota)
            print(darnota)
            self.finalAcao()

        elif option == 4:
            musica = input("Qual música você quer comentar?")
            idmusica = self.buscar_musica(musica)
            
            if idmusica is None:
                print("Música não encontrada!! Digite novamente")
                self.next(4)
            
            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = avaliar.comentar(idmusica, self.user, comentario)
            print(comt)
            self.finalAcao()
        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
    
teste = AvaliacaoInterface("6630f083927b4db79f27a5421")
teste.render()
op = int(input("Escolha uma opção: "))
teste.next(op)