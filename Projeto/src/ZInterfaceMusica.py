from AbstractMenu import *
from Music import *
from Excel import * 
from Auxiliares_uteis import *

class menuMusica(Menu):
        '''
        metodo para inicializar a interface
        '''
        self.next = None
        self.title = "Menu Musica :p"
        self.options = [
            "1 - Adicionar uma música",
            "2 - Editar música",
            "3 - Apagar música",
            "4 - Voltar ao menu anterior"
        ]
        self.options1()

        '''
        metodo para inicializar a interface
        '''
        
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

        
    def adicionar_musica(self) -> None:

        '''
        método de interface para adicionar musicas no banco de de dados
        '''
        
        while True:

            try:
            
                clear_screen()
                print("-------------------------------")
                print("Digite as informações da musica que deseja adicionar")
                
                titulo = str(input("Titulo: "))
                album = str(input("Album: "))
                numero = str(input("Numero: "))
                artista = str(input("Artista: "))
                compositores_array = input("compositores (separados por vírgula): ").split(',')
                produtores_array = input("produtores (separados por vírgula): ").split(',')
                generos_array = input("generos (separados por vírgula): ").split(',')
                duracao = str(input("Duração: "))

                musica = Musica(numero, titulo, artista, album, generos_array, compositores_array, produtores_array, duracao, 0)
                musica.adicionar_musica()
            
                adicionar_mais = input("Deseja adicionar outra música? (s/n): ").strip().lower()
                if adicionar_mais != 's':
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")
        
    def mudar_musica(self) -> None:

        '''
        método de interface para realizar alterações em uma musica no banco de dados
        '''
            
        while True:

            try:

                clear_screen()
                print("Editar musica")
                titulo = str(input("Qual o nome da musica que você deseja alterar: "))
                auxiliar = Auxiliar()
                id = auxiliar.buscar_musica(titulo)

                musica_data = getconnection.get_collection("Musica").find_one({'_id': id})
                print(musica_data)

                print("1 - Título\n 2 - Album\n 3 - Artista\n 4 - Gênero\n 5 - Compositores\n 6 - Produtores\n 7 - Duração")
                aux = str(input("Digite o valor correspontente do que você deseja alterar: "))
                mudanca = str(input("Digite a alteração "))


                if musica_data:
                    #cria uma instância com a
                    musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                    musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                    musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])

                    musica.editar_musica(musica_data['titulo'], musica_data['artista'], aux, mudanca)
                        
                else:
                    print("Música não encontrada no banco de dados.")
                    
                editar_mais = input("Deseja adicionar outra música? (s/n): ").strip().lower()
                if editar_mais != 's':
                    break

            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")
    
    def apagando_musica(self) -> None:

        '''
        método de interface responsável por apagar uma musica do banco de dados
        '''
        
        while True:
        
            try:

                print("Apagar musica")
                titulo = str(input("Qual o nome da musica que você deseja apagar: "))
                auxiliar = Auxiliar()
                id = auxiliar.buscar_musica(titulo)

                musica_data = getconnection.get_collection("Musica").find_one({'_id': id})

                if musica_data:
                    #cria musica
                    musica = Musica(musica_data['numero'], musica_data['titulo'], musica_data['artista'], 
                                            musica_data['album'], musica_data['genero'], musica_data['compositores'], 
                                            musica_data['produtores'], musica_data['duracao'], musica_data['album_id'])
                    print(musica)
                    aux = str(input("Essa é a musica que você deseja apagar? (S/N) ")).strip().lower()
                    if aux == 's':
                        musica.apagar_musica()
                    elif aux == 'n':
                        pass   
                else:
                    print("Música não encontrada.")

                
                apagar_mais = input("Deseja apagar outra música? (s/n): ").strip().lower()
                if apagar_mais != 's':
                    break
            
            except ValueError:
                print("Entrada inválida! Certifique-se de inserir os tipos de dados corretos.")



    def next(self, option: int)->None:
        
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
            self.render()
            print("Exibindo todas as musicas do banco de dados")
            Musica.exibir_musicas()
        
        else:
            print("Opção inválida! Tente novamente.")
            return None

        return self  
    

    
