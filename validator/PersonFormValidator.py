import re
from datetime import datetime

class PersonFormValidator:

    def __init__(self, firstname: str, lastname: str, birthdate: str, deathdate: str = None):
        self._errors = []
        self._has_errors = False

        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.deathdate = deathdate

    def _validate_firstname(self):

        if len(self.firstname) < 2 or len(self.firstname) > 50:
            self._errors.append("Voornaam moet tussen de 2 en 50 tekens lang zijn.")
            self._has_errors = True

        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", self.firstname):
            self._errors.append("Voornaam mag alleen letters, spaties en accenten bevatten.")
            self._has_errors = True

    def _validate_lastname(self):

        if len(self.lastname) < 2 or len(self.lastname) > 50:
            self._errors.append("Achternaam moet tussen de 2 en 50 tekens lang zijn.")
            self._has_errors = True

        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", self.lastname):
            self._errors.append("Achternaam mag alleen letters, spaties en accenten bevatten.")
            self._has_errors = True

    def _validate_birthdate(self):
        try:
            birthdate_dt = datetime.strptime(self.birthdate, "%d-%m-%Y")

            if birthdate_dt > datetime.now():
                self._errors.append("Geboortedatum kan niet in de toekomst liggen.")
                self._has_errors = True

        except ValueError:
            self._errors.append("Ongeldig datumformaat. Gebruik DD-MM-YYYY.")
            self._has_errors = True

    def _validate_deathdate(self):
        if not self.deathdate:
            return

        try:

            birthdate_dt = datetime.strptime(self.birthdate, "%d-%m-%Y")
            deathdate_dt = datetime.strptime(self.deathdate, "%d-%m-%Y")

            if birthdate_dt > deathdate_dt:
                self._errors.append("Overlijdensdatum kan niet vóór de geboortedatum liggen.")
                self._has_errors = True

            if deathdate_dt > datetime.now():
                self._errors.append("Overlijdensdatum kan niet in de toekomst liggen.")
                self._has_errors = True

        except ValueError:
            self._errors.append("Ongeldig datumformaat. Gebruik DD-MM-YYYY.")
            self._has_errors = True

    def validate(self):
        """Run all validations."""
        self._validate_firstname()
        self._validate_lastname()
        self._validate_birthdate()
        self._validate_deathdate()

    def get_errors(self):
        return self._errors, self._has_errors
