from Login import *
import sys
from Auxiliares_uteis import*
from AbstractMenu import *


class Interface_login(Menu):
    """
    Classe responsável pela interface de login do usuário.
    """
    
    def login(self):
        """
        Método para controle de login do usuário comum.
        """
        self.login_instance = Login()
        print("Vamos fazer seu login?")
        while True:
            limpar_terminal()
            self.render()
            try:
                printando_divisão()
                email = str(input("Digite seu email: "))
                printando_divisão()
                senha = str(input("Digite sua senha: "))
                result = self.login_instance.login(email, senha)
              
                if result == 4:  # Caso o retorno seja 4, o usuário foi encontrado
                    return self.login_instance.id
                # Encontra o motivo do erro, qual informação está errada
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
                print("Deseja tentar novamente querido(a)?")
                print("Digite 1 para sim e qualquer número para não")
                option = int(input())
                if option == 1:
                    limpar_terminal()
                else:
                    limpar_terminal()
                    return 0

    def render(self):
        """
        Método para renderizar a interface de login.
        """
        self.title = "Login"
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
    
    def logout(self):
        """
        Método para logout do usuário.
        """
        self.login_instance.State_update()
        return self.login_instance.state
