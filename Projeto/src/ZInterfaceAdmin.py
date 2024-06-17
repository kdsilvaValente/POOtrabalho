from AbstractMenu import *
from User import *
from Admin import * 
from ZInterfaceAlbum import *
from ZInterfaceMusica import *
from Auxiliares_uteis import *
from Excel import *

menua = menuAlbum()
auxiliar = Auxiliar()
menum = menuMusica()
excel = Excel()

class menuAdmin(Menu):
    def __init__(self):

        '''
        metodo para inicializar a interface
        '''

        self.title = "Menu de administrador :p"
        self.options = [
            "1 - Realizar alterações no banco de dados de musicas",
            "2 - Realizar alterações no banco de dados de albuns",
            "3 - Criar usuário administrador"

        ]

    def render(self) -> None:

        '''
        método para renderizar a interface
        '''

        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")

        for option in self.options:
            print(option)
            
        print("\n>> Digite sua opção")

    def next(self, option):
        
        '''
        @param option: inteiro responsável por representar a ação desejada do usuário
        metodo next: capaz de seguir o que o usuario deseja realizar
        '''
        
        clear_screen()  
        if option == 1:
            self.render()
    
            while True:

                menua.render()
                
                try:
                    option = int(input())
                except ValueError:
                    print("Por favor, insira um número válido.")
                    continue
                
                menua.next(option)

        elif option == 2:
            self.render()

            while True:

                menum.render()
                    
                try:
                    option = int(input())
                except ValueError:
                    print("Por favor, insira um número válido.")
                    continue
                    
                menum.next(option)
            
        elif option == 3:
            self.render()
            

        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
    
menu = menuAdmin()
menu.render()
opcao = int(input())
menu.next(opcao)