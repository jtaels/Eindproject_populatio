class AdresNotFoundException(Exception):
    def __init__(self, message="Adres kan niet gevonden worden!"):
        self.message = message
        super().__init__(self.message)