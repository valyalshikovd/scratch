

class Chat_data():

    def __init__(self):
        print("новый объект")
        self.login = False
        self.password = False
        self.login_exist_req = False
        self.password_exist_req = False
        self.user_data = None
        self.current_semester = ''


    def __repr__(self):
        return  "".join(map(str, [self.login, self.password, self.login_exist_req,self.password_exist_req,self.current_semester]))
