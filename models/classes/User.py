from ...run import*
class User:
    def __init__(self, name, email, password, gender, phone_number):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.phone_number = phone_number

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