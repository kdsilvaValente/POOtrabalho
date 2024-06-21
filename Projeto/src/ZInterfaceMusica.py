from AbstractMenu import *
from Music import *
from Excel import * 
from Auxiliares_uteis import *
import emoji

func_aux = Auxiliar()

class menuMusica(Menu):
    
    def __init__(self):

        '''
        método de inicialização da classe menuMusica
        '''

        self.next = 0
        self.title = "Menu Musica :p"
        self.options = [
            "1 - Adicionar uma música",
            "2 - Editar música",
            "3 - Apagar música",
            "4 - Voltar ao menu anterior",
            " "
        ]
        self.options1()

    def options1(self) -> str:

        '''
        método responsável por acessar a opção desejada pelo usuário
        '''

        while True:
            try:
                self.render()
                option = int(input("Escolha uma opção: "))
                self.options_value = option
                if 1 <= option <= 4:
                    if option != 4:
                        self.next1(option)
                    else:
                        self.next = "Voltar"
                        return
                else:
                    print(emoji.emojize("Opção inválida. Por favor, escolha uma opção de 1 a 4: "))
            except ValueError:
                print("Digite um número válido.")
        

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

        
    def adicionar_musica(self) -> None:

        '''
        método de interface para adicionar musicas no banco de de dados
        '''
        
        while True:

            try:
            
                clear_screen()
                print("=" * 30)
                print("{:^30}".format("Adicionar Música"))
                print("=" * 30)     
                print("> Digite as informações da musica que deseja adicionar")
                print(" ")

                titulo = str(input("Titulo: "))
                album = str(input("Album: "))
                numero = str(input("Numero: "))
                artista = str(input("Artista: "))
                compositores_array = input("Compositores (separados por vírgula): ").split(',')
                produtores_array = input("Produtores (separados por vírgula): ").split(',')
                generos_array = input("Gêneros (separados por vírgula): ").split(',')
                duracao = str(input("Duração: "))

                musica = Musica(numero, titulo, artista, album, generos_array, compositores_array, produtores_array, duracao, 0)
                musica.adicionar_musica()
                
                print(" ")
                print("MUSICA ADICIONADA COM SUCESSO!!!!!")

                adicionar_mais = input("> Deseja adicionar outra música? (s/n): ").strip().lower()
                if adicionar_mais != 's':
                    clear_screen()
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")

            clear_screen()


    def mudar_musica(self) -> None:

        '''
        método de interface para realizar alterações em uma musica no banco de dados
        '''
            
        while True:

            try:

                clear_screen()
                print("=" * 30)
                print("{:^30}".format("Editar Música"))
                print("=" * 30)    
                print(" ")
            
                titulo = str(input("> Qual o nome da musica que você deseja alterar: "))
                print(" ")
                auxiliar = Auxiliar()
                id = auxiliar.buscar_musica(titulo)

                musica_data = getconnection.get_collection("Musica").find_one({'_id': id})
                print(" ")



                if musica_data:
                    #cria uma instância com a
                    musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                    musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                    musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])
                    
                    print("1 - Título\n",
                    "2 - Album\n",
                    "3 - Artista\n"
                    "4 - Gênero\n"
                    "5 - Compositores\n"
                    "6 - Produtores\n"
                    "7 - Duração\n")
                
                    aux = str(input("> Digite o valor correspontente do que você deseja alterar: "))
                    auxiliar.print_info_musica(musica)
                    mudanca = str(input("> Digite a alteração: "))

                    musica.editar_musica(musica_data['titulo'], musica_data['artista'], aux, mudanca)
                        
                else:
                    print("Música não encontrada no banco de dados.")
                    
                editar_mais = input("> Deseja adicionar outra música? (s/n): ").strip().lower()
                if editar_mais != 's':
                    clear_screen()
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")
    

    def apagando_musica(self) -> None:

        '''
        método de interface responsável por apagar uma musica do banco de dados
        '''
        
        while True:
        
            try:

                print("=" * 30)
                print("{:^30}".format("Apagar Música"))
                print("=" * 30)    
                print(" ")

                
                titulo = str(input("> Qual o nome da musica que você deseja apagar: "))
                auxiliar = Auxiliar()
                id = auxiliar.buscar_musica(titulo)

                musica_data = getconnection.get_collection("Musica").find_one({'_id': id})

                if musica_data:
                    #cria musica
                    musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                            musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                            musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])

                    auxiliar.print_info_musica(musica)

                    aux = str(input("> Essa é a musica que você deseja apagar? (S/N) ")).strip().lower()
                    if aux == 's':
                        musica.apagar_musica()
                    
                else:
                    print("Música não encontrada.")

                
                apagar_mais = input("> Deseja apagar outra música? (s/n): ").strip().lower()
                if apagar_mais != 's':
                    break
            
            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")



    def next1(self, option):
        
        '''
        @param option: inteiro responsável por representar a ação desejada do usuário
        metodo next: capaz de seguir o que o usuario deseja realizar
        '''
        
        clear_screen()  
        if option == 1:
            self.render()
            self.adicionar_musica()

        elif option == 2:
            self.render()
            self.mudar_musica()
            
        elif option == 3:
            self.render()
            self.apagando_musica()

        elif option == 4:
            self.next = "Voltar"

