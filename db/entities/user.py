class User:

    def __init__(self, id, username, password, role, two_fa_secret, two_fa_enabled, last_login, created):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.two_fa_secret = two_fa_secret
        self.two_fa_enabled = two_fa_enabled
        self.last_login = last_login
        self.created = created