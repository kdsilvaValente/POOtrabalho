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
    def __init__(self, admin_id: str):
        self.admin_id = admin_id
        self.next = 0
        self.admin_user = Admin(admin_id)
        self.title = "Menu de administrador :p"
        self.options = [
            "1 - Realizar alterações no banco de dados de músicas",
            "2 - Realizar alterações no banco de dados de álbuns",
            "3 - Criar usuário administrador",
            "4 - Sair"
        ]
        self.options1()

    def options1(self) -> str:
        while True:
            try:
                self.render()
                option = int(input("Escolha uma opção: "))
                self.options_value = option
                if 1 <= option <= 4:
                    if option != 4:
                        self.next1(option)
                    else:
                        self.next = "Sair"
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 4: "))
            except ValueError:
                print("Digite um número válido.")

    def render(self) -> None:
        margem = '=' * (len(self.title) + 5)
        print(margem)
        print(f"|| {self.title} ||")
        print(margem + "\n")
        for option in self.options:
            print(option)

    def next1(self, option):
        clear_screen()
        if option == 1:
            self.next = "Musica_edição"
        elif option == 2:
            self.next = "Album_edição"
        elif option == 3:
            self.create_admin_user()
            self.next = "Admin"
        elif option == 4:
            self.next = "Sair"

    def create_admin_user(self):
        name = input("Nome do usuário a ser promovido a administrador: ")
        user_id = Admin.get_id_by_name(name)
        if user_id:
            admin = Admin(self.admin_id)
            admin.create_admin(user_id)
            print(f"Usuário {name} promovido a administrador com sucesso.")
        else:
            print("Usuário não encontrado.")