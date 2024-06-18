from AbstractMenu import *
from User import *
from Admin import *
from ZInterfaceALbum import *
from ZInterfaceMusica import *
from Auxiliares_uteis import *
from Excel import *
import emoji


menua = menuAlbum()
auxiliar = Auxiliar()
menum = menuMusica()
excel = Excel()

class menuAdmin(Menu):
    def __init__(self):
        '''
        Metodo para inicializar a interface
        '''
        self.title = "Menu de administrador :p"
        self.options = [
            "1 - Realizar alterações no banco de dados de musicas",
            "2 - Realizar alterações no banco de dados de albuns",
            "3 - Criar usuário administrador"
        ]
        self.render()

    def render(self) -> None:
        '''
        Método para renderizar a interface
        '''
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
        for option in self.options:
            print(option)
            
        print("\n>> Digite sua opção")
        try:
            opcao = int(input())
        except ValueError:
            print("Por favor, insira um número válido.")
            return self.render()
        self.next(opcao)

    def next(self, option):
        '''
        @param option: inteiro responsável por representar a ação desejada do usuário
        Metodo next: capaz de seguir o que o usuário deseja realizar
        '''
        clear_screen()  
        if option == 1:
            while True:
                menua.render()
                try:
                    option = int(input())
                except ValueError:
                    print("Por favor, insira um número válido.")
                    continue
                menua.next(option)
                break

        elif option == 2:
            while True:
                menum.render()
                try:
                    option = int(input())
                except ValueError:
                    print("Por favor, insira um número válido.")
                    continue
                menum.next(option)
                break

        elif option == 3:
            self.create_admin_user()
        else:
            print(emoji.emojize("Opção inválida. tente novamente:prohibited: "))
            self.render()

    def create_admin_user(self):
        '''
        Método para criar um novo usuário administrador
        '''
        print("Digite o nome do novo administrador:")
        nome = input()
        print("Digite a senha do novo administrador:")
        senha = input()
        
        # Adiciona a lógica de criação de um novo usuário administrador
        new_admin = Admin(nome, senha)
        print(f"Usuário administrador '{nome}' criado com sucesso!")

# menu = menuAdmin()
