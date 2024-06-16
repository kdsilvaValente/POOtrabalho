from run import getconnection 
from bson import ObjectId #biblioteca para poder usar o ObjectId e converter no formato bson

class User:
    
    def __init__(self, _id):
        self.collection = getconnection.get_collection("User")
        if _id is None:
            pass
            
        else:
            self.user_id = ObjectId(_id)
            data= self.collection.find_one({"_id":self.user_id })
            self.name=data["name"]
            self.email=data["email"]
            self.password=data["password"]
            self.gender=data["gender"]
            self.phone_number=data["phone_number"]
            self.isonline=data["isonline"]
            self.is_admin = data.get("is_admin", False)

            # Converte o ID para o formato ObjectId
    def newuser(self, userdata):
        user_data = {
                "name": userdata["name"],
                "email": userdata["email"],
                "gender": userdata["gender"],
                "phone_number": userdata["phone_number"],
                "password": userdata["password"],
                "isonline":False,
                "is_admin": userdata.get("is_admin", False)

        }
        self.collection.insert_one(user_data)

    @property
    def get_is_admin(self):
        return self.is_admin

    def delete(self):
        self.collection.find_one_and_delete({"_id": self.user_id})
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password

    def get_gender(self):
        return self.gender

    def get_phone_number(self):
        return self.phone_number
    
    from bson import ObjectId
    # atualiza os dados usando o _id
    def update_name(self, name_new):
        print(name_new)
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set": {"name": name_new}})
        self.name=name_new #melhorar futuramente, para receber do banco
        
    def update_email(self, email_new):
        print(email_new)
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set":{"email":email_new}})
        self.email=email_new

    
    def update_password(self, password_new):
        print(password_new)
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set":{"password":password_new}})
        self.password=password_new
    
    def update_gender(self, gender_new):
        print(gender_new)
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set":{"gender":gender_new}})
        self.gender=gender_new

    
    def update_number(self, phone_number_new):
        print(phone_number_new)
        self.collection.find_one_and_update({"_id": self.user_id}, {"$set":{"phone_number":phone_number_new}})
        self.phone_number=phone_number_new
    



