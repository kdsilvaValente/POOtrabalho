from User import User
import emoji
import sys  # para usar o sys.exit()
from Auxiliares_uteis import limpar_terminal, printando_divisão
from AbstractMenu import *
import re
from bson.objectid import ObjectId
from Search import*


class User_interface(Menu):
    def   __init__(self, user: dict) -> str:
        super().__init__()
        self.user = User(None)
        self.title = "PERFIL" 
        self.next = "0" #definição do next que será acessado posteriomente pela class main
        if user is not None: #verifica se o user é none, se for o caso, entra para criar um perfil novo
            self.user = User(user) #inicializando classe usuário que manipulará o banco de dados
            self.options()
        else:
            self.new_profile_interface()

    def render(self): #render padrão 
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

    def options(self) -> None: # menu de opções inicial do perfil, controla a entrada da seleção de opção e chama o menu com as opções
        while self.next == "0":
            try:
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                printando_divisão()
                if 1 <= option <= 6:
                    if option != 6:
                        self.display_main_menu_option(option)
                    else:
                        self.next = "Sair"
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 5:prohibited: "))
            except ValueError:
                print("Digite um número válido.")

    def display_main_menu(self) -> None: #printa o menu principal na tela
        printando_divisão()
        print(emoji.emojize("Bem vindo ao Menu Principal:grinning_face:"))
        print(emoji.emojize("1. Ver perfil:grinning_face_with_smiling_eyes:"))
        print(emoji.emojize("2. Editar informação do perfil:face_with_monocle:"))
        print(emoji.emojize("3. Deletar perfil:confused_face:"))
        print(emoji.emojize("4. Navegação:rocket:"))
        print(emoji.emojize("5. Gerenciar amizades:people_hugging:"))
        print(emoji.emojize("6. Sair:pirate_flag:"))
        printando_divisão()

    def display_main_menu_option(self, option: int) -> None: #direciona a função de acordo com a opção inicial escolhida
        if option == 1:
            limpar_terminal()
            self.display_user_profile()
        elif option == 2:
            limpar_terminal()
            self.update_profile()
        elif option == 3:
            limpar_terminal()
            self.delete_profile()
        elif option == 4:
            self.next = "Navegação" #definindo próximo menu como navegação
        elif option == 5:
            self.next = "Amizades" #definindo próximo menu como amizades, qe seria o gerenciamento de amizades

    def display_user_profile(self) -> None: #renderizando as informações do usuário 
        limpar_terminal()
        print("Suas informações:")
        print(f"Nome: {self.user.name}")
        print(f"Email: {self.user.email}")
        print(f"Gênero: {self.user.gender}")
        print(f"Telefone: {self.user.phone_number}")
        print(emoji.emojize(f"Status:\"{self.user.status}\"") ) 
        printando_divisão()
        self.exibir_favoritos()
    def exibir_favoritos(self):
        dados = self.user.musicas 
        if dados ==[]:
            print("você não tem músicas favoritos ainda")
        else:
            print("Musicas favoritas:")
            for i in range(len(dados)):
                search = Search("Musica")
                result = search.get_by_id(ObjectId(dados[i]))
                if result is not None:
                   print(f"{i}. {result['titulo']}")
        dados = self.user.album 
        
        if dados ==[]:
            print("você não tem albuns favoritos ainda")
        else:
            print("Albuns favoritos:")
            for i in range(len(dados)):
                search = Search("Albuns")
                result = search.get_by_id(ObjectId(dados[i]))
                if result is not None:
                     print(f"{i}. {result['album']}")

        

        
     
    def update_profile(self) -> None:  #Permite ao usuário editar as informações do perfil.

        while True: #controle de entrada para a atualização do perfil
            try:
                printando_divisão()
                print("O que deseja editar?")
                print("1. Nome")
                print("2. Email")
                print("3. Password")
                print("4. Gender")
                print("5. Phone Number")
                print("6. Status")
                print(emoji.emojize("7. Voltar :BACK_arrow: "))
                printando_divisão()

                
                choice = int(input("Escolha a opção de 1 a 7: "))
                printando_divisão()

                
                if choice == 1: #atualizando nome
                    while True:
                        new_name = input("Digite o novo nome: ")
                        if self.user.is_valid_username(new_name) == True:
                                self.user.name = new_name
                                print("Nome atualizado com sucesso!")
                                return 0
                        else:
                            print("Digite um nome válido!")
                    
                    
                elif choice == 2: #atualizando email (editar)
                    new_email =  self.chose_email()
                    self.user.email = new_email
                    print("Email atualizado com sucesso!")
                
                elif choice == 3: #atualizando senha
                    while True:
                        try:
                            current_password = input("Digite sua senha atual para confirmar: ")
                            if current_password == self.user.password: #verifica se o usuário lembra da senha atual antes de mudar
                                new_password = input("Digite sua nova senha: ")
                                self.user.password = new_password
                                print("Senha atualizada com sucesso!")
                                break
                            else:
                                print("Senha incorreta. Tente novamente.")
                        except ValueError:
                            print("Erro ao atualizar senha. Tente novamente.")
                
                elif choice == 4: #atualizando genêro
                    new_gender = self.chose_gender()  # Implemente a função chose_gender() para obter o novo gênero
                    self.user.gender = new_gender
                    print("Gênero atualizado com sucesso!")
                
                elif choice == 5: #atualizando telefone
                    new_phone = input("Digite o novo número de telefone: ")
                    self.user.phone_number = new_phone
                    print("Número de telefone atualizado com sucesso!")
                
                elif choice == 6: #atualizando status
                    new_status = input("Digite o seu novo status, consulto o dicionário de emojins caso queira!: ")
                    self.user.status = new_status
                    print("Status atualizado com sucesso!")
                
                elif choice == 7:#finaliza a função para retornar ao perfil
                    print("Retornando ao menu anterior...")
                    break
                
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 7 :prohibited: "))

            except ValueError:
                print("Opção inválida. Por favor, escolha uma opção de 1 a 7.")
            
            except Exception as e:
                print(f"Ocorreu um erro: {str(e)}")


    def chose_gender(self) -> str: #menu para escolher o gênero conforme opções idponíveis
        while True:#loop para controle de entrada
            printando_divisão()
            print("Qual seu gênero?\n")
            print("1. Mulher trans")
            print("2. Homem trans")
            print("3. Mulher cis")
            print("4. Homem cis")
            print("5. Não binário/agênero")
            print("6. Dois espíritos/Bigênero")
            print("7. Gênero neutro")
            print("8. Gênero fluído")
            printando_divisão()
            print("Escolha um número  ou aperte 9 para cancelar:\n")
            printando_divisão()


            escolha = int(input())

            if escolha >= 1 and escolha <= 8:
                if escolha == 1:
                    return "Mulher trans"
                elif escolha == 2:
                    return "Homem trans"
                elif escolha == 3:
                    return "Mulher cis"
                elif escolha == 4:
                    return "Homem cis"
                elif escolha == 5:
                    return "Não binário/agênero"
                elif escolha == 6:
                    return "Dois espíritos/Bigênero"
                elif escolha == 7:
                    return "Gênero neutro"
                elif escolha == 8:
                    return "Gênero fluído"
                elif escolha == 9:
                    return 0
            else:
                print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 8:prohibited: "))


    def new_profile_interface(self) -> None: #Cria um novo perfil para o usuário.
        printando_divisão()
        name = self.name_create()
        printando_divisão()
        email=self.chose_email()
        printando_divisão()
        gender = self.chose_gender()
        phone = str(input("Digite seu número com ddd: "))
        printando_divisão()
        password = self.chose_password()
        user_data = {
            "name": name,
            "email": email,
            "gender": gender,
            "phone_number": phone,
            "password": password,
            "isonline": False,
        }
        user = User(None)
        user.newuser(user_data) #chama a função na classe de usuário para criar o perfil
        limpar_terminal()
        print("Perfil Criado, faça seu primeiro login!")
    def name_create(self):
           while True:
             name = input("Digite o seu nome: ")
             if self.user.is_valid_username(name) == True:
                    return name
                     
             else:
                print("Digite um nome válido!")

    def chose_password(self) -> str:
        """
        Permite ao usuário escolher uma senha e a confirma.

        Returns:
            str: Senha escolhida pelo usuário.
        """
        password = "0"
        confirm_password = ""
        while True:
            while True:
                password = str(input("Escolha uma senha de pelo menos 6 dígitos e no máximo 8: "))
                if len(password) < 6 or len(password) > 8:
                    print("Mona, segue as instruções! Sua senha não condiz com o que pedimos!")
                else:
                    break

            confirm_password = str(input("Confirme sua senha: "))
            if password != confirm_password:
                print("Sua confirmação de senha não condiz com a senha escolhida, tente novamente!")
            else:
                return password


    def chose_email(self) -> str:
        """
        Permite ao usuário escolher um email válido.

        Returns:
            str: Email escolhido pelo usuário.
        """
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        chose = True
        while chose:
            email = str(input("Digite seu melhor email:"))
            if re.match(regex, email):
                chose = True
                return email
            else:
                print("Escreva um email válido.")

    def delete_profile(self) -> None:
        """
        Deleta o perfil do usuário após confirmação da senha.
        """
        while True:
            try:
                password = str(input("Confirme sua senha atual antes de deletar o perfil, ou digite 'CANCELAR' para desisitir da ação, até porque esse aplicativo é muito bom!:"))
                if password == self.user.password:
                    self.user.delete()
                    print("Perfil deletado")
                    self.next = "login"
                    return 0
                elif password == "CANCELAR":
                    return 0
                else:
                    return KeyError
            except ValueError:
                print("Senha incompatível")
       

    

