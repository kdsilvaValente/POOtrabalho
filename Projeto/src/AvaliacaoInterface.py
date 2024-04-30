from User import*
from Login import* 
from Avaliacao import*
from Album import*

class User_interface:
    def __init__(self, User):
            self.user = User
            self.options()
    def options(self):
            while True:
                  try:
                        self.display_main_menu()
                        option = int(input("Escolha uma opção: "))
                        if 1 <= option <= 4:
                            self.display_main_menu_option(option)
                        else:
                              return KeyError
                  except ValueError:
                        print("Digite um número válido")
    def display_main_menu(self):
        print("\nMenu Principal:")
        print("1. Dar like em musica")
        
    def display_main_menu_option(self,option):
           if option == 1:
            self.display_user_profile()
    
    def display_user_profile(self):
        print("\nPerfil do Usuário:")
        print(f"Nome: {self.user.get_name()}")
        print(f"Email: {self.user.get_email()}")
        print(f"Gênero: {self.user.get_gender()}")
        print(f"Telefone: {self.user.get_phone_number()}")
        self.options()



user=User("Kauan", "Kauan@", "Kauan1515", "masculino", 124563)
teste= User_interface(user)
