from Avaliacao import *
from AbstractMenu import *
from Zinterfacemain import *
from Zinterfacesearch import *
from Search import *
from run import getconnection
            
mainmenu = Interface_main()

class AvaliacaoInterface(Menu):
    def __init__(self, idUser, idmusica):
        self.user = idUser
        self.musica = idmusica
        self.title = "Vamos avaliar!"
        self.options = [
            "1 - Favoritar essa musica!!! To apaixonade nela:",
            "2 - Remover like, não gosto mais dela (emoji nojo)",
            "3 - Me sentindo crítico, quero dar nota pra essa música",
            "4 - Tenho mt a dizer!!!! Quero comentar essa música",
            "5 - Me mostre os comentários que as pessoas estão fazendo sobre essa música"
        ]

    def render(self):
        self.search.display_main_menu()
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

    
    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        avaliar = Avaliacao(getconnection)
        
        if option == 1:

            like = avaliar.darLike(self.idmusica, self.user)
            print(like)
            self.finalAcao()

        elif option == 2:

            deslike = avaliar.desfazerLike(self.idmusica, self.user)
            print(deslike)
            self.finalAcao()

        elif option == 3:
            
            nota = input("De uma a 5 estrelas, qual nota você quer dar pra essa música?")
            darnota = avaliar.darNota(self.idmusica, self.user, nota)
            print(darnota)
            self.finalAcao()

        elif option == 4:

            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = avaliar.comentar(self.idmusica, self.user, comentario)
            print(comt)
            self.finalAcao()
        
        elif option == 4:
            comentariocollection = self.__db_connection.get_collection("Comentarios")
            

        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
