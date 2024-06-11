import sys
from Zinterfacelogin import* #importando interface de login
from ZInterfaceuser import* #importando  interface de usuário
from Auxiliares_uteis import*
class Interface_main(Interface_login, User_interface):
    def initial_menu(self):
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
                        print(result)
                        if result != 0:
                            self.init_user(result)    
                    else:
                        print("Encerrando o programa.")
                        sys.exit()  
                else:
                    print("Opção inválida. Por favor, escolha uma opção de 1 a 2.")
            except ValueError:
                print("Digite um número válido.")
teste= Interface_main()
teste.initial_menu()
       