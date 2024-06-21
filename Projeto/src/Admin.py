from User import*
from run import getconnection


class Admin(User):
    
    def __init__(self, _id: str):

        '''
        @param: id do usuário que verifica se é administrador 
        '''

        super().__init__(_id)

        '''
        super init que chama os dados de user
        '''

        if not self.is_admin:
            raise PermissionError("Este usuário não é um administrador")

    
    def can_modify_admin_status(self) -> bool:

        '''
        método que retorna se usuário é ou não administrador
        '''

        return self.is_admin


    @staticmethod
    def get_id_by_name(name: str) -> str:

        '''
        @param name: string que contem o nome do usuario
        método estático responsável por acessar o ID do usuário a partir do nome
        '''

        collection = getconnection.get_collection("User")
        user = collection.find_one({"name": name})
        if user:
            return user["_id"]
        
        return None
    

    def create_admin(self, user_id: str) -> None:

        '''
        @param user_id: string que contém o id do usuário
        '''

        if not self.can_modify_admin_status():  
            raise PermissionError("Você não tem permissão para criar um administrador")

        user = self.collection.find_one({"_id": user_id})
        if user:
            self.collection.update_one(
                {"_id": user_id},
                {"$set": {"is_admin": True}}
            )
            print(f"Usuário {user['name']} promovido a administrador com sucesso")
        else:
            print("Usuário não encontrado")

    def newuser(self, userdata):
        return super().newuser(userdata)
    
    def delete(self):
        return super().delete()
    
    def get_name(self):
        return super().get_name()
    
    def get_email(self):
        return super().get_email()
    
    def get_password(self):
        return super().get_password()
    
    def get_gender(self):
        return super().get_gender()
    
    def get_phone_number(self):
        return super().get_phone_number()
    
    def update_name(self, name_new):
        return super().update_name(name_new)
    
    def update_email(self, email_new):
        return super().update_email(email_new)
    
    def update_password(self, password_new):
        return super().update_password(password_new)
    
    def update_gender(self, gender_new):
        return super().update_gender(gender_new)
    
    def update_number(self, phone_number_new):
        return super().update_number(phone_number_new)
    



