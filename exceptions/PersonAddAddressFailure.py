class PersonAddAddressFailure(Exception):
    def __init__(self, message="De persoon is niet toegevoegd aan het adres!"):
        self.message = message
        super().__init__(self.message)