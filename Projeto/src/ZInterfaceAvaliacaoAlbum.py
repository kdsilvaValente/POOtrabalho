from Avaliacao import *
from AbstractMenu import *
from Auxiliares_uteis import *
            

class AvaliacaoInterfaceAlb(InterfaceAvaliacao):
    def __init__(self, idUser, idalbum):
        self.avaliacao = Avaliacao()
        self.user = idUser
        self.album = idalbum
        self.next = None
        self.title = "Vamos avaliar!"
        self.options = [
            "1 - Favoritar esse álbum!!! Gosto muuIIiito dele:",
            "2 - Remover like, não gosto mais dele (emoji nojo)",
            "3 - Tenho mt a dizer!!!! Quero comentar esse álbum",
            "4 - Me mostre os comentários que as pessoas estão fazendo sobre esse álbum"
        ]

    def finalAcao(self):
        print("O que você deseja fazer agora?")
        print("1 - Fazer outra pesquisa")
        print("2 - Mais ações com esse álbum!")

        next_option = int(input("Escolha uma opção: "))

        if next_option == 1:
            self.next = "Navegação"

        elif next_option == 2:
            self.next = "Album"
            self.render()
            opcao = int(input("Digite a opção desejada: "))
            self.next1(opcao)
        else:
            print("Opção inválida.")
            self.finalAcao()


    def iniciotela(self):
        print("Abrindo o álbum!! Aqui estão as informações dele:")
        album = self.avaliacao.validar_album(self.album)
        if "favoritados" in album:
            print(f"O album {album['album']} foi favoritado {album['favoritados']} vezes!")
        else:
            print(f"O album {album['album']} não foi favoritado ainda... Mude isso!!")
        print(f"De {album['artista']}, ele possui as seguintes faixas:")
        if "musicas" in album:
            for i, musica in enumerate(album["musicas"]):
                if i == len(album["musicas"]) - 1:
                    print(f"e {musica}.")
                    print("==========================================================")
                else:
                    print(f"{musica},")
        

        while True:
            bool_str = input("Deseja avaliar esse álbum? Responda com 1 para sim e 0 para não:\n")
            if bool_str == '1':
                self.render()
                opcao = int(input("Digite a opção desejada:"))
                self.next1(opcao)
                break  # Sai do loop enquanto a opção for válida
            elif bool_str == '0':
                print("Beleza! Voltando ao menu principal...")
                print("...")
                print("...")
                print("...")
                self.next = "Navegação"
                break  # Sai do loop enquanto a opção for válida
            else:
                print("Opção inválida, tente novamente.")
    
    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)
    
    def next1(self, option: int):
        clear_screen()  # limpa a tela ao iniciar um novo menu
        
        if option == 1:
            like = self.avaliacao.favoritarAlbum(self.album, self.user)
            print(like)
            print("==========================================================")
            self.finalAcao()

        elif option == 2:
            deslike = self.avaliacao.desfavoritarAlbum(self.album, self.user)
            print(deslike)
            print("==========================================================")
            self.finalAcao()

        elif option == 3:
            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = self.avaliacao.comentar(self.album, self.user, comentario)
            print(comt)
            print("==========================================================")
            self.finalAcao()
        
        elif option == 4:
            comments = self.avaliacao.exibirComentariosAlbum()
            print(comments)
            print("==========================================================")
            self.finalAcao()

        else:
            print("Opção inválida! Tente novamente.")
            op = int(input("Escolha uma opção válida: "))
            self.next1(op)

        return self