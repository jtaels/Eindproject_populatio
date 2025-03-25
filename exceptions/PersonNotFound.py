class PersonNotFoundException(Exception):
    def __init__(self, message="Persoon kan niet gevonden worden!"):
        self.message = message
        super().__init__(self.message)