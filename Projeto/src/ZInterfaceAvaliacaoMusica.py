from Avaliacao import *
from AbstractMenu import *
#from Zinterfacesearch import Interface_search
#from Zinterfacemain import Interface_main
from run import getconnection
from Auxiliares_uteis import *


#mainmenu = Interface_main()
avaliacao = Avaliacao(getconnection)
#search = Interface_search()

class AvaliacaoInterMsc(Menu):
    def __init__(self, idUser, idmusica, idalbum):
        self.avaliacao = Avaliacao(getconnection)
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

    def iniciotela(self):
        print("Abrindo a música!! Aqui estão as informações dela:")
        musica = self.avaliacao.validar_musica(self.musica)
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
                self.render()
                opcao = input("Digite a opção desejada:")
                self.next(opcao)
                break  # Sai do loop enquanto a opção for válida
            elif bool_str == '0':
                print("Beleza! Voltando ao menu principal...")
                print("...")
                print("...")
                print("...")
                #mainmenu.initial_menu()
                break  # Sai do loop enquanto a opção for válida
            else:
                print("Opção inválida, tente novamente.")
        

    def render(self):
        self.search.display_main_menu()
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.optionsmusic:
            print(option)
    
    def finalAcao(self):
        print("deu certo até aqiui")
        # print("O que você deseja fazer agora?")
        # print("1 - Voltar ao menu principal")
        # print("2 - Fazer outra pesquisa")

        # next_option = input("Escolha uma opção: ")

        # if next_option == '1':
        #     mainmenu.initial_menu()
        #     option = int(input("Escolha uma opção: "))
        #     mainmenu.init_user_main(self.user)

        # elif next_option == '2':
        #     search.display_main_menu()
        #     option = int(input("Escolha uma opção: "))
        #     self.next(option)
            
        # else:
        #     print("Opção inválida.")
        #     self.finalAcao()

    
    def next(self, option):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        avaliar = Avaliacao(getconnection)
        
        if option == 1:

            like = avaliar.darLike(self.musica, self.user)
            print(like)
            self.finalAcao()

        elif option == 2:

            deslike = avaliar.desfazerLike(self.musica, self.user)
            print(deslike)
            self.finalAcao()

        elif option == 3:
            
            nota = input("De uma a 5 estrelas, qual nota você quer dar pra essa música?")
            darnota = avaliar.darNota(self.musica, self.user, nota)
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

teste = AvaliacaoInterMsc("666881d43c864f1f7af7caef", "666f314eba8d12c50e7b33c6", "666f314eba8d12c50e7b33c5")
teste.iniciotela()
op = teste.render()
teste.next(op)
teste.finalAcao
