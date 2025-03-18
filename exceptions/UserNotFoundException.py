class UserNotFoundException(Exception):
    def __init__(self, message="Gebruiker niet gevonden"):
        self.message = message
        super().__init__(self.message)