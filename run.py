from models.connection_options.connection import DBconnectionHandler

db_handle= DBconnectionHandler()
db_handle.connect_to_db()
getconnection = db_handle.get_db_connection()
print(getconnection)
collection = getconnection.get_collection('teste')
print(collection)

