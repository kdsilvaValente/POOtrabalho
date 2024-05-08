from User import*
from Login import* 
import emoji
import sys #para usar o sys.exit()


class User_interface:
    def init_user(self,user):
            self.user=User(user)
            self.options()
            
    def options(self):
        while True:
            try:
                self.display_main_menu()
                option = int(input("Escolha uma opção: "))
                if 1 <= option <= 4:
                     if option !=4:
                        self.display_main_menu_option(option)
                     else:
                        print("Encerrando o programa.") 
                        sys.exit()#corrigindo bug de encerrar programanda
                               
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 4.")
            except ValueError:
                print("Digite um número válido.")

    def display_main_menu(self):
        print("-------------------------------")
        print(emoji.emojize('Bem vindo ao Menu Principal:grinning_face:: '))
        print("1. Ver perfil")
        print("2. Editar informação do perfil")
        print("3. Deletar perfil")
        print("4. Sair")
        #opções de navegação, e a opção sair precisa direcionar para a tela principal
        print("-------------------------------")
    def display_main_menu_option(self,option):
           if option == 1:
            self.display_user_profile()
           if option == 2:
            self.update_profile()
           if option == 3:
             self.delete_profile()
           

            
    
    def display_user_profile(self):
        print("-------------------------------")
        print("\nSeu perfil:")
        print(f"Nome: {self.user.get_name()}")
        print(f"Email: {self.user.get_email()}")
        print(f"Gênero: {self.user.get_gender()}")
        print(f"Telefone: {self.user.get_phone_number()}")
        print("-------------------------------")
        self.options()
    def update_profile(self):
        while True:
            try:
                print("-------------------------------")
                print("O que deseja editar?")
                print("1. Nome")
                print("2. Email")
                print("3. Password")
                print("4. Gender")
                print("5. Phone Number")
                choice = int(input("Escolha a opção de 1 a 5: "))
                print("-------------------------------")

            

                if choice == 1:
                    new_name = str(input("Digite o novo nome: "))
                    self.user.update_name(new_name)
                elif choice == 2:
                    email_new = str(input("Digite o novo email: "))
                    self.user.update_email(email_new)
                elif choice == 3:
                    while True:
                        try:
                            password=str(input("Confirme sua senha atual antes de editar:"))
                            if password == self.user.get_password():
                                new_password = str(input("Senha correta, digite sua nova senha: "))
                                self.user.update_password(new_password)
                            else:
                                return KeyError
                            self.options()
                        except ValueError:
                            print("Senha incompatível")
                elif choice == 4:
                    new_gender=self.chose_gender()
                    self.user.update_gender(new_gender)
                elif choice == 5:
                    new_phone = int(input("Digite o novo número de telefone: "))
                    self.user.update_number(new_phone)
                self.options()
            except ValueError:
                print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")

    def chose_gender(self):
        while True:
            print("Qual seu gênero?\n")
            print("1. Mulher trans")
            print("2. Homem trans")
            print("3. Mulher cis")
            print("4. Homem cis")
            print("5. Não binário/agênero")
            print("6. Dois espíritos/Bigênero")
            print("7. Gênero neutro")
            print("8. Gênero fluído")
            print("Escolha um número:\n")

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
            else:
                print("Opção inválida. Por favor, escolha um número entre 1 e 8.")

    def delete_profile(self):
          while True:
            try:
                password=str(input("Confirme sua senha atual antes de deletar o perfil:"))
                if password == self.user.get_password():
                    self.user.delete()
                    print("Perfil deletado")
                else:
                    return KeyError
                self.options()
            except ValueError:
                print("Senha incompatível")


# userdata={
#           "name":"Natasha",
#           "email":"natashacaldeirão@gmail.com" ,
#           "gender":"Gênero neutro",
#           "phone_number":11984587624,
#           "password": "Natashaarrasa",
#           }
teste = User_interface()
teste.init_user("66323501e31fdfa9372dda6a")



            
            
         


                        
          
                


