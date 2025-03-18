import re

class RegisterFormValidator:

    def __init__(self, username: str, password: str, password_repeat: str):
        self._errors = {

        }
        self._has_errors = False
        self.username = username
        self.password = password
        self.password_repeat = password_repeat

    def _validate_username(self):

        if "username" not in self._errors:
            self._errors["username"] = []

        # Is de gebruikersnaam tussen de 3 en 20 karakters?
        if len(self.username) < 3 or len(self.username) > 20:
            self._errors["username"].append("De gebruikersnaam moet tussen de 3 en 20 tekens zijn.")
            self._has_errors = True

        # Controleren op de juiste karakters (alleen letters, cijfers en underscores)
        if not re.match(r"^[a-zA-Z0-9_]+$", self.username):
            self._errors["username"].append("De gebruikersnaam mag alleen letters, cijfers en underscores bevatten.")
            self._has_errors = True

    def _validate_password(self):

        if "password" not in self._errors:
            self._errors["password"] = []

        # Minimaal 8 tekens
        if len(self.password) < 8:
            self._errors["password"].append("Het wachtwoord moet minstens 8 tekens lang zijn.")
            self._has_errors = True

        # Minstens één hoofdletter
        if not re.search(r"[A-Z]", self.password):
            self._errors["password"].append("Het wachtwoord moet minstens één hoofdletter bevatten.")
            self._has_errors = True

        # Minstens één kleine letter
        if not re.search(r"[a-z]", self.password):
            self._errors["password"].append("Het wachtwoord moet minstens één kleine letter bevatten.")
            self._has_errors = True

        # Minstens één cijfer
        if not re.search(r"\d", self.password):
            self._errors["password"].append("Het wachtwoord moet minstens één cijfer bevatten.")
            self._has_errors = True

        # Minstens één speciaal teken
        if not re.search(r"[!@#$%^&*()_+{}[\]:;\"'<>,.?/~\\]", self.password):
            self._errors["password"].append("Het wachtwoord moet minstens één speciaal teken bevatten (!@#$%^&* etc.).")
            self._has_errors = True

        # Wachtwoorden moeten overeenkomen
        if self.password != self.password_repeat:
            self._errors["password"].append("De wachtwoorden komen niet overeen.")
            self._has_errors = True

    def validate(self):
        """Voer alle validaties uit."""
        self._validate_username()
        self._validate_password()

    def get_errors(self):

        return self._errors,self._has_errors