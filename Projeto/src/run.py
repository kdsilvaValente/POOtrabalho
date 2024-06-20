from connection_options.connection import DBconnectionHandler

db_handle= DBconnectionHandler()
db_handle.connect_to_db()
getconnection = db_handle.get_db_connection() #realiza a conexão com albumagic no banco de dados




