class PersonCreateFailureException(Exception):
    def __init__(self, message="Fout bij het aanmaken van de persoon!"):
        self.message = message
        super().__init__(self.message)