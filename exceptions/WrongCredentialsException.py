class WrongCredentialsException(Exception):
    def __init__(self, message="Gebruikersnaam of wachtwoord is verkeerd!"):
        self.message = message
        super().__init__(self.message)