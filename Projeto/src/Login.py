from run import getconnection

class Login:
    def login(self,email, password):
        self.collection = getconnection.get_collection("User")
        
        # Verifica se o usuário já existe no banco de dados com base no número na senha e e-mail
        search = {
             "password": password,
            "email": email,
        }
        isthere_user = self.collection.find_one(search)
        #realiza o login se o usuário existe e a senha e email está correto
        if isthere_user is not None:
          print(f"Bem vindo {isthere_user['name']}")
          return isthere_user

        #verifica a causa do erro ao logar, se é a senha, o email, ou ambos
        else:
             search_password = {
             "password": password,
            }
             isthere_password = self.collection.find_one(search_password)
             search_email = {
               "email": email,
                }
             isthere_email = self.collection.find_one(search_email)
             if isthere_password is None and isthere_email is not None:
                 print("Senha incorreto ou usuário inexistente")       
             
             if isthere_email is None and isthere_password is not None:
                 print("Email incorreto ou usuário inexistente")
             if isthere_email is None and isthere_password is None:
                 print("Dados incorretos ou usuário inexistente")

login=Login()
login.login("yuriwada@gmail.com", "euamookauan")
                 
                
           
            
           


