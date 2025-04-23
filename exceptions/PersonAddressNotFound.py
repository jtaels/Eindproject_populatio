class PersonAddressNotFound(Exception):
    def __init__(self, message="Kan het persoonsadres niet vinden!"):
        self.message = message
        super().__init__(self.message)