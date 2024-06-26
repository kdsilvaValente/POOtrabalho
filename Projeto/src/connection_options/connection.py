from pymongo import MongoClient, errors # Certifique-se de que pymongo.errors esteja corretamente importado #importação do pymongo, biblioteca que possibilita a integração do python com o banco de dados
from .mongo_db_configs import mongo_db_infos 
# from mongo_db_configs import mongo_db_infos
from urllib.parse import quote_plus #uso do quote_plus para "traduzir" os símbolos gráficos na hora da leitura feita pelo MongoClient

class DBconnectionHandler: 
    def __init__(self) -> None: #construtora da classe DBconnectionHandler, responsável por gerenciar o controle da conexão
        # username = "pooalbumatic" #se tem o congigs, para que colocar essas variáveis aqui? /lucas
        # password = "tr@balhopoo"
        username = mongo_db_infos["USERNAME"]
        password = mongo_db_infos["PASSWORD"] 
        self.__connection_string = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@cluster0.lb2khsh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.dbname = mongo_db_infos["DB_NAME"]
        self.__client = None
        self.__db_connection = None

    
 
    def connect_to_db(self):
        # Função para realizar a conexão inicial com o banco de dados
        try:
            self.__client = MongoClient(self.__connection_string)
            self.__db_connection = self.__client[quote_plus(self.dbname)]
            return True
        except (errors.ConnectionFailure, errors.ConfigurationError, ValueError) as e:
            self.__client = None
            self.__db_connection = None
            return False

  
        #     print( self.__db_connection)
    def get_db_connection(self):# retorno da conexão feita, últil para confirmar a conexão 
            return self.__db_connection 
    def get_db_client(self):
            return self.__client
 






