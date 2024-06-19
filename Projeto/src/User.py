from run import getconnection
from bson import ObjectId
from typing import Optional, Dict
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional
import re

class User:
    
    def __init__(self, _id: Optional[str]) -> None:
        self.collection = getconnection.get_collection("User")
        if _id is None:
            pass
        else:
            self.user_id = ObjectId(_id)
            self.data = self.collection.find_one({"_id": self.user_id})
            if self.data:
                self._name = self.data["name"]
                self._email = self.data["email"]
                self._password = self.data["password"]
                self._gender = self.data["gender"]
                self._phone_number = self.data["phone_number"]
                self._isonline = self.data["isonline"]
                self._is_admin = self.data["is_admin"]
                self._lista_amigos = self.data["friends"]
                self._lista_pedidos = self.data["ask_friends"]
                self._lista_favoritos = self.data.get("favoritos", [])
                self._status = self.data.get("status", "")
                self.teste_parametros()
            else:
                raise ValueError("Usuário não encontrado com o ID fornecido.")

    def sharefavorites(self):
        pass
    
    def newuser(self, userdata: dict[str, str]) -> None:
        if not isinstance(userdata, dict):
            raise TypeError("O parâmetro 'userdata' deve ser um dicionário.")
        user_data = {
            "name": userdata["name"],
            "email": userdata["email"],
            "gender": userdata["gender"],
            "phone_number": userdata["phone_number"],
            "password": userdata["password"],
            "isonline": False,
            "is_admin": userdata.get("is_admin", False),
            "friends": [], 
            "ask_friends": [],
            "favoritos": [],
            "status": "Adicione seu status"  # Adicionando status ao criar um novo usuário
        }
        self.collection.insert_one(user_data) 
    def is_valid_username(self,username): #verifica se o nome é válido
        # Verifica se o nome de usuário contém apenas letras (maiúsculas ou minúsculas)
        if re.fullmatch(r'[A-Za-z]+', username):
            return True
        else:
            return False
    def teste_parametros(self):
        # Verifica se favoritos não está presente e adiciona se necessário
        if "favoritos" not in self.data:
            self.collection.update_one(
                {"_id": self.user_id},
                {"$set": {"favoritos": []}}
            )
        # Verifica se status não está presente e adiciona se necessário
        if "status" not in self.data:
            self.collection.update_one(
                {"_id": self.user_id},
                {"$set": {"status": ""}}
            )

    def delete(self) -> None:
        self.collection.find_one_and_delete({"_id": self.user_id})

    def excluir_amigo(self, id) -> None:
        self.collection.update_one(
            {'_id':  self.user_id },
            {'$pull': {'friends': ObjectId(id)}}
        )
        self.collection.update_one(
            {'_id':  ObjectId(id)},
            {'$pull': {'friends': self.user_id}}
        )

    def pedir_amizade(self, id) -> None:
        self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$push': {'ask_friends': self.user_id}}
        )

    def aceitar_pedido(self, id) -> None:
        self.collection.update_one(
            {'_id': self.user_id},
            {'$push': {'friends': ObjectId(id)}}
        )
        self.collection.update_one(
            {'_id': self.user_id},
            {'$pull': {'ask_friends': ObjectId(id)}}
        )
        self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$push': {'friends':  self.user_id}}
        )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"name": value}})
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"email": value}})
        self._email = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"password": value}})
        self._password = value
    
    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"gender": value}})
        self._gender = value

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"phone_number": value}})
        self._phone_number = value

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def lista_amigos(self) -> str:
        return self._lista_amigos

    @property
    def lista_pedidos(self) -> str:
        return self._lista_pedidos

    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"status": value}})
        self._status = value  # Corrigido para atualizar corretamente _status

    @property
    def isadmin(self) -> str:
        return self._is_admin
    
