from User import*

class Admin(User):

    def __init__(self, _id):
        super().__init__(_id)
        if not self.is_admin:
            raise PermissionError("nao eh admin")

    def create_admin(self, userdata):
        if not self.is_admin:
            raise PermissionError("apenas admin adiciona")
        userdata["is_admin"] = True
        self.newuser(userdata)
        print("admin criado")

    
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
    



