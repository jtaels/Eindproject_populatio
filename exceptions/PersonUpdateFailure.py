class PersonUpdateFailureException(Exception):
    def __init__(self, message="Fout bij het bewerken van de persoon!"):
        self.message = message
        super().__init__(self.message)