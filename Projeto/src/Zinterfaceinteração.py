import sys
from Auxiliares_uteis import *
from AbstractMenu import *
from User import *
from Search import*  
from bson.objectid import ObjectId
import emoji


class Interface_interação(Menu):
    def __init__(self, user: str, user_pesquisa: str = None) -> str:
        """
        Inicializa a interface de interação.

        :param user: ID do usuário atual.
        :param user_pesquisa: ID do usuário a ser pesquisado (opcional).
        """
        self.search = Search("User")
        self.next = "0"  # definição do next que será acessado posteriomente pela class main
        self.user = User(user)
        self.title = "INTERAÇÃO"
        if user_pesquisa is None:  # verifica se o user_pesquisa é None, pois se for, o usuário não quer ver um perfil específico 
            self.options()
        else:
            self.ver_perfil(user_pesquisa)

    def options(self) -> None:
        """
        Menu de opções inicial do perfil, controla a entrada da seleção de opção e chama o menu com as opções.
        """
        while self.next == "0":  # loop para controle de entrada
            try:
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                printando_divisão()
                if 1 <= option <= 3:
                    if option != 3:
                        self.display_main_menu_option(option)
                    else:
                        self.next = "Perfil"
                        print("Voltando ao perfil...")
                        return 
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 3:prohibited: "))
            except ValueError:
                print("Digite um número válido.")
    
    def display_main_menu(self) -> None:
        """
        Printa o menu principal na tela.
        """
        print(emoji.emojize("1. Ver lista de amigos :people_hugging:"))
        print(emoji.emojize("2. Ver lista de pedidos de amizade :envelope:"))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        printando_divisão()
    
    def display_main_menu_option(self, option: int) -> None:
        """
        Direciona a função de acordo com a opção inicial escolhida.

        :param option: Opção escolhida pelo usuário.
        """
        if option == 1:
            self.ver_amigos()
        elif option == 2:
            self.ver_pedidos()
        elif option == 3:
            self.next = "Perfil"
     
    def ver_perfil(self, id: str) -> None:
        """
        Abre o perfil de um usuário específico.

        :param id: ID do usuário a ser visualizado.
        """
        result = self.search.get_by_id(ObjectId(id))
        if result is not None:
            print(f"Nome: {result.get('name', '')}")
            print(f"Gênero: {result['gender']}")
            status = "online" if result['isonline'] else "offline"
            print(emoji.emojize(f"Situação: {status}"))
            print(emoji.emojize(f"Status: \"{result['status']}\""))
        else:
            pass

        
        while True:  # loop para controle de entrada
            try:
                option = int(input("Deseja pedir amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.pedir_amizade(ObjectId(id))
                        return 0
                    else:
                        limpar_terminal()
                        self.next = "Amizades"  # define amizades como próximo menu
                        return
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")
    def ver_perfil_2(self, id: str) -> None:
        """
        Abre o perfil de um usuário específico.

        :param id: ID do usuário a ser visualizado.
        """
        result = self.search.get_by_id(ObjectId(id))
        print(f"Nome: {result['name']}")
        print(f"Gênero: {result['gender']}")
        status = "online" if result['isonline'] else "offline"
        print(emoji.emojize(f"Situação: {status}"))
        print(emoji.emojize(f"Status: \"{result['status']}\""))
        user_amigo = id
        user_amigo_abrir = User(id)
        dados = user_amigo_abrir.musicas 
        if dados ==[]:
            print(f"{result['name']} não tem músicas favoritos ainda")
        else:
            print("Musicas favoritas:")
            number=1
            for i in range(len(dados)):
                search = Search("Musica")
                result = search.get_by_id(ObjectId(dados[i]))
                if result is not None and result is not "":
                   print(f"{number}. {result['titulo']}")
                   number+=1
        user_amigo = id
        user_amigo_abrir = User(id)
        dados = user_amigo_abrir.album 
        
        if dados ==[]:
            print(f"{result['name']} não tem albuns favoritos ainda")
        else:
            print("Albuns favoritos:")
            number=1
            for i in range(len(dados)):
                search = Search("Albuns")
                result = search.get_by_id(ObjectId(dados[i]))
                if result is not None:
                     print(f"{number}. {result['album']}")
                     number+=1

        option = int(input("Clique qualquer tecla para voltar: "))
        limpar_terminal()
        self.next = "Amizades"  # define amizades como próximo menu
        return 0
              
    def pedir_amizade(self, id: ObjectId) -> None:
        """
        Realiza o pedido de amizade a um usuário.

        :param id: ID do usuário para quem enviar o pedido de amizade.
        """
        self.user.pedir_amizade(id)  # faz a mudança no banco
        print(emoji.emojize("Pedido realizado com sucesso:rocket:!"))
        self.next = "Amizades"
    
    def aceitar_amizade(self, amizades: list) -> None:
        """
        Aceita o pedido de amizade de um usuário.

        :param amizades: Lista de IDs de usuários que enviaram pedidos de amizade.
        """
        while True:
            escolha = int(input("Qual amizade você deseja aceitar?: "))
            if not testar_tamanho_vetor(len(amizades), escolha):
               pass
            else:
                self.user.aceitar_pedido(amizades[escolha-1])
                self.next = "Amizades"
                result = self.search.get_by_id(ObjectId(self.user.lista_pedidos[escolha-1]))
                print(f"Agora você e {result['name']} são amigos!")
                return 0 

    def ver_amigos(self) -> None:
        """
        Renderiza a lista de amigos do usuário.
        """
        if not self.user.lista_amigos:
            print("você não tem um amigo ainda, continue navegando e faça novas amizades!")
        else:
            length = len(self.user.lista_amigos)
            for i in range(length):
                result = self.search.get_by_id((self.user.lista_amigos[i]))
                if result == None:
                    print("você não tem um amigo ainda, continue navegando e faça novas amizades!")
                    return 0
                else:
                    print(f"{i+1}: {result['name']}")
            self.amigos(self.user.lista_amigos)

    def amigos(self, friends: list) -> None:
        """
        Renderiza opções após ver a lista de amigos disponíveis.

        :param friends: Lista de IDs dos amigos do usuário.
        """
        printando_divisão()
        print(emoji.emojize("1. Ver perfil de algum amigo :people_hugging: "))
        print(emoji.emojize("2. Desfazer amizade com algum amigo :cross_mark: "))
        print(emoji.emojize("3. Voltar :BACK_arrow: "))
        printando_divisão()
        while True:
            try:
                option = int(input("Escolha uma opção: "))
                if 1 <= option <= 3:
                    if option == 1:
                        while True:
                            escolha = int(input("Qual perfil deseja ver? Digite o número:  "))
                            if not testar_tamanho_vetor(len(friends), escolha):
                                pass
                            else:
                                self.ver_perfil_2(friends[escolha-1])
                                self.next = "Amizades"
                                return 0 
                    elif option == 2:
                        self.excluir_amigo(friends)
                        return
                    else:
                        limpar_terminal()
                        self.next = "Amizades"  
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 3:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def ver_pedidos(self) -> None:
        """
        Renderiza os pedidos de amizade recebidos.
        """
        length = len(self.user.lista_pedidos)
        for i in range(length):
            result = self.search.get_by_id(ObjectId(self.user.lista_pedidos[i]))
            if result == None:
                print("você não tem um pedidos ainda, continue navegando e faça novas amizades!")
                return 0
            else:
                print(f"{i+1}: {result['name']}")
                
        while True:
            try:
                if not self.user.lista_pedidos:
                    print("Você não tem nenhum pedido ainda, continue navegando e faça amigos!")
                    option = 2
                else:
                    option = int(input("Deseja aceitar alguma amizade?\n1. Sim\n2. Não, retornar\nEscolha uma opção: "))
                if 1 <= option <= 2:
                    if option == 1:
                        self.aceitar_amizade(self.user.lista_pedidos)
                        return 0
                    else:
                        self.next = "Amizades"
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 2:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def excluir_amigo(self, amizades: list) -> None:
        """
        Seleciona e exclui uma amizade.

        :param amizades: Lista de IDs dos amigos do usuário.
        """
        while True:
            escolha = int(input("Qual amizade você deseja desfazer?: "))
            if not testar_tamanho_vetor(len(amizades), escolha):
               pass
            else:
                self.user.excluir_amigo(amizades[escolha-1])
                self.next = "Amizades"
                print("Amizade desfeita!")
                return 0 
    
    def render(self) -> None:
        """
        Render padrão da interface.
        """
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
