from run import collection  # supondo que collection esteja definida em run.py

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
        }
        # Inserindo o usuário no banco de dados
        result = collection.insert_one(user_data)
        find = collection.find_one({"name": name})
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
        print(self.name)
        print(name_new)
        collection.find_one_and_update({"name":self.name}, {"$set":{"name":name_new}})
        result=collection.find_one({"name": name_new})
        print(result["name"])

        
    

teste = User("Valente", "kauan@gmail.com.br", "Kauan55485", "male", "11 54521365")

teste.update_name("Silva")


