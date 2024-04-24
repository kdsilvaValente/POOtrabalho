from run import getconnection  # supondo que collection esteja definida em run.py

class User:
    def __init__(self, name, email, password, gender, phone_number):
        self.collection = getconnection.get_collection("User")
        
        # Verifica se o usuário já existe no banco de dados com base no número de telefone e e-mail
        search = {
            "phone_number": phone_number,
            "email": email,
        }
        isthere_user = self.collection.find_one(search)
        
        # Se o usuário não existir, insere os dados do novo usuário no banco de dados
        if isthere_user is None:
            user_data = {
                "name": name,
                "email": email,
                "gender": gender,
                "phone_number": phone_number,
                "password": password,
            }
            self.collection.insert_one(user_data)
            print("adicionado")
        else:
            self.name = isthere_user["name"]
            self.email = isthere_user["email"]
            self.password = isthere_user["password"]
            self.gender = isthere_user["gender"]
            self.phone_number = isthere_user["phone_number"]
            print(f"Bem vindo {self.name}")

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email


    def get_gender(self):
        return self.gender

    def get_phone_number(self):
        return self.phone_number
    
    def update_name(self, name_new):
        print(name_new)
        self.collection.find_one_and_update({"name":self.name}, {"$set":{"name":name_new}})
    
    def update_email(self, email_new):
        print(email_new)
        self.collection.find_one_and_update({"email":self.email}, {"$set":{"email":email_new}})
    
    def update_password(self, password_new):
        print(password_new)
        self.collection.find_one_and_update({"password":self.password}, {"$set":{"password":password_new}})
    
    def update_gender(self, gender_new):
        print(gender_new)
        self.collection.find_one_and_update({"gender":self.gender}, {"$set":{"gender":gender_new}})
    
    def update_number(self, phone_number_new):
        print(phone_number_new)
        self.collection.find_one_and_update({"phone_number":self.phone_number}, {"$set":{"phone_number":phone_number_new}})
       
       

        
    



