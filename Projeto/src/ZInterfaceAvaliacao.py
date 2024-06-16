from Avaliacao import *
from AbstractMenu import *
from Zinterfacemain import *
from Zinterfacesearch import *
from Search import *
from run import getconnection
            
mainmenu = Interface_main()
avaliacao = Avaliacao(getconnection)
search = Interface_search()

class AvaliacaoInterface(Menu):
    def __init__(self, idUser, idmusica, idalbum):
        self.user = idUser
        self.musica = idmusica
        self.album = idalbum
        self.title = "Vamos avaliar!"
        self.optionsmusic = [
            "1 - Favoritar essa musica!!! To apaixonade nela:",
            "2 - Remover like, não gosto mais dela (emoji nojo)",
            "3 - Me sentindo crítico, quero dar nota pra essa música",
            "4 - Tenho mt a dizer!!!! Quero comentar essa música",
            "5 - Me mostre os comentários que as pessoas estão fazendo sobre essa música"
        ]

        self.optionsalbum = [
            "1 - Favoritar esse álbum!!! Gosto muuIIiito dele:",
            "2 - Remover like, não gosto mais dele (emoji nojo)",
            "4 - Tenho mt a dizer!!!! Quero comentar essa música",
            "5 - Me mostre os comentários que as pessoas estão fazendo sobre esse álbum"
        ]


    def inicioMusicOptions(self, idMusica: ObjectId):
        print("Abrindo a música!! Aqui estão as informações dela:")
        musica = avaliacao.validar_musica(idMusica)
        if musica["likes"]:
            print(f"A musica {musica["titulo"]} tem {musica["likes"]} likes!")
        else:
            print(f"A musica {musica["titulo"]} não foi favoritada ainda... Mude isso!!")
        print("Outras informaçõess sobre ela!! Veja:")
        print(f"Ela é a faixa {musica["numero"]} do álbum {musica["album"]}")
        
        if musica["produtores"]:
            print("Foi produzida por:")
            for produtor in musica["produtores"]:
                print(f"{produtor},\n")
            else:
                print("Não há produtores! :( Sabe-se lá como essa música veio ao mundo")

        if musica["compositores"]:
            print("Foi composta por:")
            for compositor in musica["compositores"]:
                print(f"{compositor},\n")
            else:
                print("Não há compositores! Um caso de escritor fantasma em nossas mãos")
        
        print("A música é do(s) gênero(s):")
        for gen in musica["genero"]:
            print(f"{gen},\n")
        
        print(f"Duração de {musica["duracao"]}")
        
        if musica["avaliacao final"]:
            print(f"A média da avaliação dos usuários dessa música é de {musica["avaliacao final"]} estrelas!")
        else:
            print(f"A musica {musica["titulo"]} não foi avaliada ainda... Mude isso!!")
        
        while True:
            bool_str = input("Deseja avaliar a música? Responda com 1 para sim e 0 para não:\n")
            if bool_str == '1':
                self.renderMusic()
                opcao = input("Digite a opção desejada:")
                self.nextMusic(opcao)
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
        

    def renderMusic(self):
        self.search.display_main_menu()
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.optionsmusic:
            print(option)
    
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

    
    def nextMusic(self, option):
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
            comt = avaliar.comentarAlbum(self.album, self.user, comentario)
            print(comt)
            self.finalAcao()


        elif option == 5:
            comentariocollection = self.__db_connection.get_collection("Comentarios")
            comentarios = comentariocollection.find_many({"musica": ObjectId(self.musica)})
            for comentario in comentarios:
                print(comentarios["comentario"])

        else:
            print("Opção inválida! Tente novamente.")
            self.finalAcao()

        return self  

    def inicioAlbunsOptions(self, idAlbum: ObjectId):
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
                self.renderAlbum()
                opcao = input("Digite a opção desejada:")
                self.nextAlbum(opcao)
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
    
    def renderAlbum(self):
        self.search.display_main_menu()
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.optionsalbum:
            print(option)
    
    def nextAlbum(self, option):
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
