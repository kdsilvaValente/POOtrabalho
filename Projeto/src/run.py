from connection_options.connection import DBconnectionHandler

db_handle= DBconnectionHandler()
db_handle.connect_to_db()
getconnection = db_handle.get_db_connection()
collection = getconnection.get_collection('User')
# print(collection)

search_filter = {"estou": "aqui"}
response = collection.find(search_filter)

for registry in response: print(registry)



