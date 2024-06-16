from run import getconnection
from bson import ObjectId
from typing import Optional, Dict

class User:
    
    def __init__(self, _id: Optional[str]) -> None:
        self.collection = getconnection.get_collection("User")
        if _id is None:
            pass
        else:
            self.user_id = ObjectId(_id)
            data = self.collection.find_one({"_id": self.user_id})
            if data:
                self._name = data["name"]
                self._email = data["email"]
                self._password = data["password"]
                self._gender = data["gender"]
                self._phone_number = data["phone_number"]
                self._isonline = data["isonline"]
                self.is_admin = data.get("is_admin", False)

            else:
                raise ValueError("Usuário não encontrado com o ID fornecido.")
    
    def newuser(self, userdata: Dict[str, str]) -> None:
        if not isinstance(userdata, dict):
            raise TypeError("O parâmetro 'userdata' deve ser um dicionário.")
        user_data = {
            "name": userdata["name"],
            "email": userdata["email"],
            "gender": userdata["gender"],
            "phone_number": userdata["phone_number"],
            "password": userdata["password"],
            "isonline": False,
            "isadmin": data.get("is_admin", False)
        }
        self.collection.insert_one(user_data)

    def delete(self) -> None:
    
        self.collection.find_one_and_delete({"_id": self.user_id})
    
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
