from run import getconnection  # supondo que collection esteja definida em run.py

class User:
    def __init__(self, name, email, password, gender, phone_number):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.phone_number = phone_number
        user_data = {
            "name": name,
            "email": email,
            "gender": gender,
            "phone_number": phone_number,
            "password": password,
        }
        # Inserindo o usuário no banco de dados
        self.collection = getconnection.get_collection("User")
        result = self.collection.insert_one(user_data)
        find = self.collection.find_one({"name": name})
        print(find["email"])



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
    
    def update_name(self, name_new):
        print(name_new)
        self.collection.find_one_and_update({"name":self.name}, {"$set":{"name":name_new}})
    
    def update_email(self, email_new):
        print(email_new)
        self.collection.find_one_and_update({"email":self.email}, {"$set":{"email":email_new}})
    
    def update_name(self, password_new):
        print(password_new)
        self.collection.find_one_and_update({"password":self.password}, {"$set":{"password":password_new}})
    
    def update_name(self, gender_new):
        print(gender_new)
        self.collection.find_one_and_update({"gender":self.gender}, {"$set":{"gender":gender_new}})
    
    def update_name(self, phone_number_new):
        print(phone_number_new)
        self.collection.find_one_and_update({"phone_number":self.phone_number}, {"$set":{"phone_number":phone_number_new}})
       
       

        
    

teste = User("Valente", "kauan@gmail.com.br", "Kauan55485", "male", "11 54521365")

teste.update_name("Silva")


