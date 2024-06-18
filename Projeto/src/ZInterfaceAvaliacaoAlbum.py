from Avaliacao import *
from AbstractMenu import *
from Zinterfacemain import *
from Zinterfacesearch import *
from Search import *
from run import getconnection
            
avaliacao = Avaliacao(getconnection)
search = Interface_search()

class AvaliacaoInterfaceAlb(Menu):
    def __init__(self, idUser, idmusica, idalbum):
        self.user = idUser
        self.musica = idmusica
        self.album = idalbum
        self.title = "Vamos avaliar!"
        self.options = [
            "1 - Favoritar esse álbum!!! Gosto muuIIiito dele:",
            "2 - Remover like, não gosto mais dele (emoji nojo)",
            "4 - Tenho mt a dizer!!!! Quero comentar essa música",
            "5 - Me mostre os comentários que as pessoas estão fazendo sobre esse álbum"
        ]
        
    def finalAcao(self):
        print("O que você deseja fazer agora?")
        print("1 - Voltar ao menu principal")
        print("2 - Fazer outra pesquisa")

        next_option = input("Escolha uma opção: ")

        if next_option == '1':
            mainmenu.initial_menu()
            option = int(input("Escolha uma opção: "))
            mainmenu.init_user_main(self.user)

        elif next_option == '2':
            search.display_main_menu()
            option = int(input("Escolha uma opção: "))
            self.nextMusic(option)
            
        else:
            print("Opção inválida.")
            self.finalAcao()


    def iniciotela(self, idAlbum: ObjectId):
        print("Abrindo o álbum!! Aqui estão as informações dele:")
        album = avaliacao.validar_musica(idAlbum)
        if album["favoritados"]:
            print(f"O album {album['album']} foi favoritado {album['favoritados']} vezes!")
        else:
            print(f"O album {album["album"]} não foi favoritado ainda... Mude isso!!")
        print("Outras informações sobre o álbum!! Veja:")
        print(f"De {album['artista']}, ele possui as seguintes faixas:")
        faixas = album.get('faixas', [])
        for idx, faixa in enumerate(faixas, start=1):
            print(f"{idx} - {faixa}")
        print("Deseja favoritar esse álbum?")

        while True:
            bool_str = input("Deseja avaliar esse álbum? Responda com 1 para sim e 0 para não:\n")
            if bool_str == '1':
                self.render()
                opcao = input("Digite a opção desejada:")
                self.next(opcao)
                break  # Sai do loop enquanto a opção for válida
            elif bool_str == '0':
                print("Beleza! Voltando ao menu principal...")
                print("...")
                print("...")
                print("...")
                mainmenu.initial_menu()
                break  # Sai do loop enquanto a opção for válida
            else:
                print("Opção inválida, tente novamente.")
    
    def render(self):
        self.search.display_main_menu()
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)
    
    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        avaliar = Avaliacao(getconnection)
        
        if option == 1:

            like = avaliar.favoritarAlbum(self.album, self.user)
            print(like)
            self.finalAcao()

        elif option == 2:

            deslike = avaliar.desfavoritarAlbum(self.album, self.user)
            print(deslike)
            self.finalAcao()

        elif option == 3:

            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = avaliar.comentar(self.idmusica, self.user, comentario)
            print(comt)
            self.finalAcao()
        
        elif option == 4:
            comentariocollection = self.__db_connection.get_collection("Comentarios")
            comentarios = comentariocollection.find_many({"albun": ObjectId(self.album)})
            for comentario in comentarios:
                print(comentarios["comentario"])
            self.finalAcao()

        else:
            print("Opção inválida! Tente novamente.")
            self.finalAcao()

        return self  
