from pymongo import MongoClient
from urllib.parse import quote_plus

# Dados de conexão
username = "pooalbumatic"
password = "tr@balhopoo"

connection_string = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@cluster0.lb2khsh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)

db_connection = client["albumatic"]

print(db_connection)

collection = db_connection.get_collection("collection")

print(collection)
print()

search_filter = {"estou": "aqui"}
response = collection.find(search_filter)

for registry in response: print(registry)

collection.insert_one({
    "estou": "inserindo",
    "numeros": [123, 456, 789]
})