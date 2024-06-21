from run import getconnection
from bson import ObjectId
from typing import Optional, Dict
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional
import re

class User:
    
    def __init__(self, _id: Optional[str]) -> None:
        """
        :param _id: id do usuário
        """
        self.collection = getconnection.get_collection("User") #realiza a conexão no banco de dados com a collection de usuários
        if _id is None: #verifica se id é none, caso seja, apenas acaba a função
            pass
        else: #caso id não seja none, os dados são minerados do banco
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
                self._musicas = self.data.get("musicas_curtidas", [])
                self._album = self.data.get("albuns_favoritados", [])
                self.teste_parametros()
            else:
                raise ValueError("Usuário não encontrado com o ID fornecido.")

    def sharefavorites(self):
        pass
    
    def newuser(self, userdata: dict[str, str]) -> None:
        """
        :param userdata: dados do usuário novo
        cria um novo usuário no banco de dados
        """
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
    def is_valid_username(self,username):
        """

        :param username: nome do usuário que será testado antes de atualizar ou de adicionar ao banco
        verifica se o nome é válido
        Verifica se o nome de usuário contém apenas letras (maiúsculas ou minúsculas)
        """
        if re.fullmatch(r'[A-Za-z]+', username):
            return True
        else:
            return False
    def teste_parametros(self):
        """
        verifica a existência dos campos no banco e adiciona caso não exista, muito útil para futuras manutenções, evitando ter que alterar 
        cada objeto da collection user de uma vez
        """
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

        if "musicas_curtidas" not in self.data:
            self.collection.update_one(
                {"_id": self.user_id},
                {"$set": {"musicas_curtidas": []}}
            )
        
        if "albuns_favoritados" not in self.data:
            self.collection.update_one(
                {"_id": self.user_id},
                {"$set": {"albuns_favoritados": []}}
            )
    def delete(self) -> None:
        """
        deleta usuário do banco de dados
        """
        self.collection.find_one_and_delete({"_id": self.user_id})

    def excluir_amigo(self, id) -> None:
        """
        :param id: id do usuário que será desfeito a amizade em relação ao usuário atual do sistema
        desfaz a amizade, de forma bilateral, alterando os dois objetos envolvidos
        """
        self.collection.update_one(
            {'_id':  self.user_id },
            {'$pull': {'friends': ObjectId(id)}}
        )
        self.collection.update_one(
            {'_id':  ObjectId(id)},
            {'$pull': {'friends': self.user_id}}
        )

    def pedir_amizade(self, id) -> None:
        """
        :param id: id a quem o usuário deseja enviar um pedido de amizade
        """
        self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$push': {'ask_friends': self.user_id}}
        )

    def aceitar_pedido(self, id) -> None:
        """
        :param id: id do usuário que será feita a amizade em relação ao usuário atual do sistema
        cria uma amizade, de forma bilateral, alterando os dois objetos envolvidos
        """
        #adicionando id a lista de amigos do usuário
        self.collection.update_one(
            {'_id': self.user_id},
            {'$push': {'friends': ObjectId(id)}}
        )
        #removendo o pedido de amizade da lista de amigos do usuário
        self.collection.update_one(
            {'_id': self.user_id},
            {'$pull': {'ask_friends': ObjectId(id)}}
        )
        #adicionando id do usuário na lista de amigos do usuário com o id recebido 
        self.collection.update_one(
            {'_id': ObjectId(id)},
            {'$push': {'friends':  self.user_id}}
        )

    @property
    def name(self) -> str:
        """
        retorna o nome do usuário
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        :param value: novo nome do usuário
        edita  o nome do usuário
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"name": value}})
        self._name = value

    @property
    def email(self) -> str:
        """
        retorna o email do usuário
        """
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        :param value: novo email do usuário
        edita o email do usuário
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"email": value}})
        self._email = value


    @property
    def password(self) -> str:
        """
        Retorna a senha do usuário.
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        :param value: Nova senha do usuário.
        Edita a senha do usuário.
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"password": value}})
        self._password = value

    @property
    def gender(self) -> str:
        """
        Retorna o gênero do usuário.
        """
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        """
        :param value: Novo gênero do usuário.
        Edita o gênero do usuário.
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"gender": value}})
        self._gender = value

    @property
    def phone_number(self) -> str:
        """
        Retorna o número de telefone do usuário.
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        """
        :param value: Novo número de telefone do usuário.
        Edita o número de telefone do usuário.
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"phone_number": value}})
        self._phone_number = value

    @property
    def is_admin(self) -> bool:
        """
        Retorna se o usuário é administrador.
        """
        return self._is_admin

    @property
    def lista_amigos(self) -> str:
        """
        Retorna a lista de amigos do usuário.
        """
        return self._lista_amigos

    @property
    def lista_pedidos(self) -> str:
        """
        Retorna a lista de pedidos do usuário.
        """
        return self._lista_pedidos

    @property
    def status(self) -> str:
        """
        Retorna o status do usuário.
        """
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        """
        :param value: Novo status do usuário.
        Edita o status do usuário.
        """
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"status": value}})
        self._status = value

    @property
    def musicas(self) -> str:
        """
        Retorna as musicas favoritas usuário.
        """
        return self._musicas
    
    @property
    def album(self) -> str:
        """
        Retorna as musicas favoritas usuário.
        """
        return self._album

    

    