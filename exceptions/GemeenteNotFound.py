class GemeenteNotFoundException(Exception):
    def __init__(self, message="Gemeente kan niet gevonden worden!"):
        self.message = message
        super().__init__(self.message)