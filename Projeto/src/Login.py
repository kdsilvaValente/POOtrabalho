from run import getconnection

class Login:
    def __init__(self) -> None:
        self._iduser=0
    def login(self, email, password):
        self.collection = getconnection.get_collection("User")        
        # Verifica se o usuário já existe no banco de dados com base na senha e e-mail
        search = {
            "password": password,
            "email": email,
        }
        self.isthere_user = self.collection.find_one(search)
        result= self.ist_here_user(email,password )
        if result == 4:
            self.collection.find_one_and_update(
                {"_id": self.isthere_user["_id"]}, 
                {"$set": {"isonline": True}}
            )
            self._iduser= self.isthere_user["_id"]
            return result
        else:
            return result
      

    def State_update(self):
          self.collection.find_one_and_update(
                {"_id": self.isthere_user["_id"]}, 
                {"$set": {"isonline": False}}
            )
    def ist_here_user(self, email, password):
        search_password = {
            "password": password,
        }
        isthere_password = self.collection.find_one(search_password)
        
        search_email = {
            "email": email,
        }
        isthere_email = self.collection.find_one(search_email)
        if isthere_email == None:
            return 1
        if isthere_password is None and isthere_email is not None:
            return 2
        if isthere_email is None and isthere_password is None:
            return 3
        return 4 
    def get_id(self):
        return self._iduser


