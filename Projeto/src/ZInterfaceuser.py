from User import User
import emoji
import sys  # para usar o sys.exit()
from Auxiliares_uteis import limpar_terminal
from AbstractMenu import *
import re


class User_interface(Menu):
    def init_user(self, user: dict) -> str:
        """
        Inicia a interface do usuário com base nos dados fornecidos.

        Args:
            user (dict): Dicionário contendo os dados do usuário.

        Returns:
            str: Retorna a próxima ação a ser realizada após a interação com o usuário.
        """
        self.title = "PERFIL"
        self.next = "0"
        if user is not None:
            self.user = User(user)
            self.options()
            return self.next
        else:
            self.new_profile_interface()

    def render(self):
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

    def options(self) -> None:
        """
        Mostra as opções disponíveis no menu principal e lida com a escolha do usuário.
    
        """
        re
        while self.next == "0":
            try:
                limpar_terminal()
                self.render()
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                print("-------------------------------")
                if 1 <= option <= 5:
                    if option != 5:
                        self.display_main_menu_option(option)
                    else:
                        self.next = "Sair"
                        return
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
            except ValueError:
                print("Digite um número válido.")

    def display_main_menu(self) -> None:
        """
        Mostra o menu principal na tela.
        """
        print("-------------------------------")
        print(emoji.emojize("Bem vindo ao Menu Principal :grinning_face:"))
        print("1. Ver perfil")
        print("2. Editar informação do perfil")
        print("3. Deletar perfil")
        print("4. Navegação")
        print("5. Sair")
        print("-------------------------------")

    def display_main_menu_option(self, option: int) -> None:
        """
        Mostra a opção escolhida pelo usuário do menu principal.

        Args:
            option (int): Opção escolhida pelo usuário.
        """
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
            self.next = "Navegação"

    def display_user_profile(self) -> None:
        """
        Mostra o perfil atual do usuário na tela.
        """
        limpar_terminal()
        print("Seu perfil:")
        print(f"Nome: {self.user.name}")
        print(f"Email: {self.user.email}")
        print(f"Gênero: {self.user.gender}")
        print(f"Telefone: {self.user.phone_number}")

    def update_profile(self) -> None:
        """
        Permite ao usuário editar as informações do perfil.
        """
        while True:
            try:
                print("-------------------------------")
                print("O que deseja editar?")
                print("1. Nome")
                print("2. Email")
                print("3. Password")
                print("4. Gender")
                print("5. Phone Number")
                print("6. Voltar")
                print("-------------------------------")
                choice = int(input("Escolha a opção de 1 a 5: "))
                print("-------------------------------")

                if choice == 1:
                    new_name = str(input("Digite o novo nome: "))
                    self.user.name = new_name
                    print("Nome atualizado com sucesso!")
                    break

                elif choice == 2:
                    email_new = str(input("Digite o novo email: "))
                    self.user.email = email_new
                    print("Email atualizado com sucesso!")
                    break

                elif choice == 3:
                    while True:
                        try:
                            password = str(input("Confirme sua senha atual antes de editar: "))
                            if password == self.user.password:
                                new_password = str(input("Senha correta, digite sua nova senha: "))
                                self.user.password = new_password
                                print("Senha atualizada com sucesso!")
                                break
                            else:
                                print("Senha incorreta. Tente novamente.")
                        except ValueError:
                            print("Erro ao atualizar senha. Tente novamente.")
                    break

                elif choice == 4:
                    new_gender = self.chose_gender()
                    self.user.gender = new_gender
                    print("Gênero atualizado com sucesso!")
                    break

                elif choice == 5:
                    new_phone = int(input("Digite o novo número de telefone: "))
                    self.user.phone_number = new_phone
                    print("Número de telefone atualizado com sucesso!")
                    break
                elif choice == 6:
                    return 0


                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")

            except ValueError:
                print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")
            except Exception as e:
                print(f"Ocorreu um erro: {str(e)}")

    def chose_gender(self) -> str:
        """
        Permite ao usuário escolher seu gênero.

        Returns:
            str: Gênero escolhido pelo usuário.
        """
        while True:
            print("-------------------------------")
            print("Qual seu gênero?\n")
            print("1. Mulher trans")
            print("2. Homem trans")
            print("3. Mulher cis")
            print("4. Homem cis")
            print("5. Não binário/agênero")
            print("6. Dois espíritos/Bigênero")
            print("7. Gênero neutro")
            print("8. Gênero fluído")
            print("-------------------------------")
            print("Escolha um número  ou aperte 9 para cancelar:\n")
            print("-------------------------------")


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
                print("Opção inválida. Por favor, escolha um número entre 1 e 8.")

    def new_profile_interface(self) -> None:
        """
        Cria um novo perfil para o usuário.
        """
        print("-------------------------------")
        name = str(input("Qual seu nome?: "))
        print("-------------------------------")
        email = str(input("Digite seu email: "))
        print("-------------------------------")
        gender = self.chose_gender()
        phone = int(input("Digite seu número com ddd: "))
        print("-------------------------------")
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
        user.newuser(user_data)
        limpar_terminal()
        print("Perfil Criado")

    def chose_password(self) -> str:
        """
        Permite ao usuário escolher uma senha e a confirma.

        Returns:
            str: Senha escolhida pelo usuário.
        """
        password = "0"
        confirm_password = ""
        while password != confirm_password:
            password = str(input("Escolha uma senha: "))
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
                password = str(input("Confirme sua senha atual antes de deletar o perfil:"))
                if password == self.user.get_password():
                    self.user.delete()
                    print("Perfil deletado")
                else:
                    return KeyError
            except ValueError:
                print("Senha incompatível")
    


