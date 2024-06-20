from Avaliacao import *
from AbstractMenu import *
from Auxiliares_uteis import *

class AvaliacaoInterMsc(InterfaceAvaliacao):
    def __init__(self, idUser, idmusica):
        """
        Inicializa a interface de avaliação de músicas.

        :param idUser: ID do usuário.
        :param idmusica: ID da música.
        """
        self.avaliacao = Avaliacao()
        self.user = idUser
        self.musica = idmusica
        self.next = None
        self.conexao = getconnection
        self.title = "Vamos avaliar!"
        self.optionsmusic = [
            "1 - Favoritar essa musica!!! To apaixonade nela:",
            "2 - Remover like, não gosto mais dela (emoji nojo)",
            "3 - Me sentindo crítico, quero dar nota pra essa música",
            "4 - Tenho mt a dizer!!!! Quero comentar essa música",
            "5 - Me mostre os comentários que as pessoas estão fazendo sobre essa música"
        ]
        
    def iniciotela(self):
        """
        Exibe as informações da música e pergunta se o usuário deseja avaliá-la.
        """
        print("Abrindo a música!! Aqui estão as informações dela:")
        musica = self.avaliacao.validar_musica(self.musica)
        if "likes" in musica:
            print(f"A música {musica['titulo']} tem {musica['likes']} likes!")
            print("==========================================================")
        else:
            print(f"A música {musica['titulo']} não foi favoritada ainda... Mude isso!!")
            print("==========================================================")

        print("Outras informações sobre ela!! Veja:")
        print(f"Ela é a faixa {musica['numero']} do álbum {musica['album']}.")
        print("==========================================================")
        
        if "produtores" in musica:
            print("Foi produzida por:")
            for i, produtor in enumerate(musica["produtores"]):
                if i == len(musica["produtores"]) - 1:
                    print(f"e {produtor}.")
                else:
                    print(f"{produtor},")
            print("==========================================================")
        else:
            print("Não há produtores! :( Sabe-se lá como essa música veio ao mundo")
            print("==========================================================")
        
        if "compositores" in musica:
            print("Foi composta por:")
            for i, compositor in enumerate(musica["compositores"]):
                if i == len(musica["compositores"]) - 1:
                    print(f"e {compositor}.")
                    print("==========================================================")
                else:
                    print(f"{compositor},")
        else:
            print("Não há compositores! Um caso de escritor fantasma em nossas mãos")
            print("==========================================================")
        
        if "genero" in musica: 
            i = len(musica["genero"])
            if i == 1:
                print(f"O gênero dessa música é {musica['genero']}!")
            elif i > 1:
                print("A música pertence a esses gêneros:")
                for i, gen in enumerate(musica["genero"]):
                    if i == len(musica["genero"]) - 1:
                        print(f"e {gen}.")
                    else:
                        print(f"{gen},")
                print("==========================================================")
            else:
                print("Essa música é tão diferente que não consigo pensar em um gênero pra ela...")
                print("==========================================================")
                
        print(f"Duração de {musica['duracao']}")
        print("==========================================================")
        if "avaliacao final" in musica:
            print(f"A média da avaliação dos usuários dessa música é de {musica['avaliacao final']} estrelas!")
            print("==========================================================")
        else:
            print(f"A música {musica['titulo']} não foi avaliada ainda... Mude isso!!")
            print("==========================================================")

        while True:
            bool_str = input("Deseja avaliar a música? Responda com 1 para sim e 0 para não:\n")
            if bool_str == '1':
                self.render()
                opcao = int(input("Digite a opção desejada: "))
                self.next1(opcao)
                break  # Sai do loop enquanto a opção for válida
            elif bool_str == '0':
                print("Beleza! Voltando ao menu!")
                print("...")
                print("...")
                print("...")
                self.next = "Navegação"
                break  # Sai do loop enquanto a opção for válida
            else:
                print("Opção inválida, tente novamente.")
        
    def render(self):
        """
        Renderiza o menu de opções para avaliação da música.
        """
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.optionsmusic:
            print(option)
    
    def finalAcao(self):
        """
        Exibe as opções finais após uma ação e processa a escolha do usuário.
        """
        print("deu certo até aqui")
        print("O que você deseja fazer agora?")
        print("1 - Fazer outra pesquisa")
        print("2 - Avaliar essa mesma música novamente")

        next_option = int(input("Escolha uma opção: "))

        if next_option == 1:
            self.next = "Navegação"
        elif next_option == 2:
            self.next = "Musica"
            self.render()
            opcao = int(input("Digite a opção desejada: "))
            self.next1(opcao)
        else:
            print("Opção inválida.")
            self.finalAcao()

    def next1(self, option: int):
        """
        Processa a opção escolhida pelo usuário no menu de avaliação.

        :param option: Opção escolhida pelo usuário.
        """
        clear_screen()  # limpa a tela ao iniciar um novo menu
        
        if option == 1:
            like = self.avaliacao.darLike(self.musica, self.user)
            print(like)
            print("==========================================================")
            self.finalAcao()
        elif option == 2:
            deslike = self.avaliacao.desfazerLike(self.musica, self.user)
            print(deslike)
            print("==========================================================")
            self.finalAcao()
        elif option == 3:
            nota = int(input("De uma a 5 estrelas, qual nota você quer dar pra essa música?"))
            darnota = self.avaliacao.darNota(self.musica, self.user, nota)
            print(darnota)
            print("==========================================================")
            self.finalAcao()
        elif option == 4:
            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = self.avaliacao.comentar(self.musica, self.user, comentario)
            print(comt)
            print("==========================================================")
            self.finalAcao()
        elif option == 5:
            comments = self.avaliacao.exibirComentarios()
            print(comments)
            self.finalAcao()
        else:
            op = int(input("Opção inválida! Tente novamente."))
            self.next1(op)

        return self
