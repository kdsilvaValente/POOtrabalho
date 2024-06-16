from Login import *
import sys
from Auxiliares_uteis import*


class Interface_login:          
    def login(self):
        self.login_instance = Login()
        print("Vamos fazer seu login?")
        while True:
            try:
                print("-------------------------------")
                email = str(input("Digite seu email: "))
                print("-------------------------------")
                senha = str(input("Digite sua senha: "))
                result = self.login_instance.login(email, senha)
              
                if result == 4: # caso o retorno seja 4, o usuário foi encontrado 
                    return self.login_instance.id
                #encontra o motivo do erro, qual informação está errada
                elif result == 1:
                    print("Email incorreto ou usuário inexistente") 
                    raise Exception
                elif result == 2:
                    print("Senha incorreta ou usuário inexistente")  
                    raise Exception
                else:
                    print("Dados incorretos ou usuário inexistente")
                    raise Exception
            except Exception as e:
                print("Erro:", e)
                print("Deseja tentar novamente?")
                print("1. Sim")
                print("2. Não")
                option=int(input())
                if option == 2:
                  limpar_terminal
                  return 0
    def logout(self):
        self.login_instance.State_update()
        return self.login_instance.state
    





