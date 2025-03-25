class User:

    def __init__(self, id:int, username:str, password:str, role:int, two_fa_secret:str, two_fa_enabled:int, last_login:str, created:str):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.two_fa_secret = two_fa_secret
        self.two_fa_enabled = two_fa_enabled
        self.last_login = last_login
        self.created = created