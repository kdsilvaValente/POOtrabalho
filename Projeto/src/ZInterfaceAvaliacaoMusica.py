from Avaliacao import *
from AbstractMenu import *
from Auxiliares_uteis import *

class AvaliacaoInterMsc(InterfaceAvaliacao):
    def __init__(self, idUser: str, idmusica: str)->None:
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
            "1. Favoritar essa musica!!! To apaixonade nela:",
            "2. Remover like, não gosto mais dela (emoji nojo)",
            "3. Me sentindo crítico, quero dar nota pra essa música",
            "4. Tenho mt a dizer!!!! Quero comentar essa música",
            "5. Me mostre os comentários que as pessoas estão fazendo sobre essa música",
            "6. Exibir novamente as informações da música"
        ]
        
    def iniciotela(self)->None:
        """
        Exibe as informações da música e pergunta se o usuário deseja avaliá-la.
        """
        print("Abrindo a música!! Aqui estão as informações dela:")
        musica = self.avaliacao.validar_musica(self.musica)
        if "likes" in musica:
            print(f"A música {musica['titulo']} tem {musica['likes']} likes!")
            printando_divisão_2()
        else:
            print(f"A música {musica['titulo']} não foi favoritada ainda... Mude isso!!")
            printando_divisão_2()

        print("Outras informações sobre ela!! Veja:")
        print(f"Ela é a faixa {musica['numero']} do álbum {musica['album']}.")
        printando_divisão_2()
        
        if "produtores" in musica:
            print("Foi produzida por:")
            for i, produtor in enumerate(musica["produtores"]):
                if i == len(musica["produtores"]) - 1:
                    print(f"e {produtor}.")
                else:
                    print(f"{produtor},")
            printando_divisão_2()
        else:
            print("Não há produtores! :( Sabe-se lá como essa música veio ao mundo")
            printando_divisão_2()
        
        if "compositores" in musica:
            print("Foi composta por:")
            for i, compositor in enumerate(musica["compositores"]):
                if i == len(musica["compositores"]) - 1:
                    print(f"e {compositor}.")
                    printando_divisão_2()
                else:
                    print(f"{compositor},")
        else:
            print("Não há compositores! Um caso de escritor fantasma em nossas mãos")
            printando_divisão_2()
        
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
                printando_divisão_2()
            else:
                print("Essa música é tão diferente que não consigo pensar em um gênero pra ela...")
                printando_divisão_2()
                
        print(f"Duração de {musica['duracao']}")
        printando_divisão_2()
        if "avaliacao final" in musica:
            print(f"A média da avaliação dos usuários dessa música é de {musica['avaliacao final']} estrelas!")
            printando_divisão_2()
        else:
            print(f"A música {musica['titulo']} não foi avaliada ainda... Mude isso!!")
            printando_divisão_2()

        while True:
            bool_str = input("Deseja realizar alguma ação nessa música? Responda com 1 para sim e 0 para não:\n")
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
        
    def render(self)->None:
        """
        Renderiza o menu de opções para avaliação da música.
        """
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.optionsmusic:
            print(option)
    
    def finalAcao(self)->None:
        """
        Exibe as opções finais após uma ação e processa a escolha do usuário.
        """
        print("O que você deseja fazer agora?")
        print("1 - Fazer outra pesquisa")
        print("2 - Voltar")

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

    def next1(self, option: int)->None:
        """
        Processa a opção escolhida pelo usuário no menu de avaliação.

        :param option: Opção escolhida pelo usuário.
        """
        
        if option == 1:
            like = self.avaliacao.darLike(self.musica, self.user)
            print(like)
            printando_divisão_2()
            self.finalAcao()
        elif option == 2:
            deslike = self.avaliacao.desfazerLike(self.musica, self.user)
            print(deslike)
            printando_divisão_2()
            self.finalAcao()
        elif option == 3:
            while True:
                nota = int(input("De 1 a 5 estrelas, qual nota você quer dar pra essa música?"))
                if nota >5 or nota<0:
                    print("digite uma nota válida!")
                    pass
                else:
                    darnota = self.avaliacao.darNota(self.musica, self.user, nota)
                    print(darnota)
                    printando_divisão_2()
                    self.finalAcao()
                    return 0
        elif option == 4:
            comentario = input("Sou todo ouvidos! Me conta o que você tem a dizer:")
            comt = self.avaliacao.comentar(self.musica, self.user, comentario)
            print(comt)
            printando_divisão_2()
            self.finalAcao()
        elif option == 5:
            comments = self.avaliacao.exibirComentarios(self.musica)
            for comment in comments:
                print(comment)
            printando_divisão_2()
            self.finalAcao()
        elif option == 6:
            self.iniciotela()
        else:
            op = int(input("Opção inválida! Tente novamente."))
            self.next1(op)

        return self
