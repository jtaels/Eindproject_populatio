class CreateGemeenteFailed(Exception):
    def __init__(self, message="Gemeente is niet aangemaakt!"):
        self.message = message
        super().__init__(self.message)