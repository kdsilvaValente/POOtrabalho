from run import getconnection 
from bson import ObjectId #biblioteca para poder usar o ObjectId e converter no formato bson

class User:
    def __init__(self, _id):
        self.collection = getconnection.get_collection("User")
        self.user_id = ObjectId(_id)
        data= self.collection.find_one({"_id":self.user_id })
        print("cheguei")
    
        print(data)
        self.name=data["name"]
        self.email=data["email"]
        self.password=data["password"]
        self.gender=data["gender"]
        self.phone_number=data["phone_number"]
        self.isonline=data["isonline"]
        # Converte o ID para o formato ObjectId
    def newuser(self, userdata):
        user_data = {
                "name": userdata["name"],
                "email": userdata["email"],
                "gender": userdata["gender"],
                "phone_number": userdata["phone_number"],
                "password": userdata["password"],
                "isonline": userdata["isonline"],
        }
        self.collection.insert_one(user_data)
        print("adicionado")
        
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
    def chose_gender(self):
        while True:
            print("Qual seu gênero?\n")
            print("1. Mulher trans")
            print("2. Homem trans")
            print("3. Mulher cis")
            print("4. Homem cis")
            print("5. Não binário/agênero")
            print("6. Dois espíritos/Bigênero")
            print("7. Gênero neutro")
            print("8. Gênero fluído")
            print("Escolha um número:\n")

            escolha = int(input())

            if escolha >= 1 and escolha <= 8:
                if escolha == 1:
                    return "Mulher trans"
                elif escolha == 2:
                    return "Homem trans"
                elif escolha == 3:
                    return "Mulher cis"
                elif escolha == 4:
                    return "Homem cis"
                elif escolha == 5:
                    return "Não binário/agênero"
                elif escolha == 6:
                    return "Dois espíritos/Bigênero"
                elif escolha == 7:
                    return "Gênero neutro"
                elif escolha == 8:
                    return "Gênero fluído"
            else:
                print("Opção inválida. Por favor, escolha um número entre 1 e 8.")


    
   



        
    



