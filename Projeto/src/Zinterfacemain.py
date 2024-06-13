import sys
from Zinterfacelogin import* #importando interface de login
from ZInterfaceuser import* #importando  interface de usuário
from Auxiliares_uteis import*
class Interface_main(Interface_login, User_interface):
    def __init__(self) -> None:
        self.result = None
    def initial_menu(self): # menu principal 
         while True:
            try:
                limpar_terminal()
                print("Bem-vindo ao albumatic, o que deseja fazer?")
                print("1.Login")
                print("2.Criar perfil")
                option = int(input())
                limpar_terminal()
                if 1 <= option <= 2:
                    if option ==1:
                        result =self.login()
                        if result != 0:
                            self.result=result
                            self.init_user_main(result)    
                    else:
                        self.init_user(None)
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")
    def init_user_main(self, result): # menu para chamar o menu user 
            self.init_user(result)

teste= Interface_main()
teste.initial_menu()
       