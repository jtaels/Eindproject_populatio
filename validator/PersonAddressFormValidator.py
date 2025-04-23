import re
from datetime import datetime

class PersonAddressFormValidator:

    def __init__(self, adres_type:str,date_from:str=None, date_to:str=None):
        self._errors = []
        self._has_errors = False

        self.valid_address_types = [
            "Hoofdverblijfplaats",
            "Tijdelijk verblijf",
            "Instelling",
            "Verblijf bij familie / mantelzorg",
            "Vakantieverblijf / tweede verblijf",
            "Asielopvang / opvangcentrum"
        ]

        self.adres_type = adres_type
        self.date_from = date_from
        self.date_to = date_to

    def _validate_address_type(self):

        if self.adres_type not in self.valid_address_types:
            self._errors.append("Ongeldig adressoort!")
            self._has_errors = True

    def _validate_date_from(self):

        if self.date_from:

            try:

                datetime.strptime(self.date_from, "%d-%m-%Y")

            except ValueError:
                self._errors.append("Ongeldig datumformaat. Gebruik DD-MM-YYYY.")
                self._has_errors = True


    def _validate_date_to(self):

        if self.date_to:

            try:
                date_from_obj = datetime.strptime(self.date_from, "%d-%m-%Y")
                date_to_obj = datetime.strptime(self.date_to, "%d-%m-%Y")

                if date_from_obj > date_to_obj:
                    self._errors.append("Datum 'wonend sinds' kan niet later zijn dan de verhuis datum!")
                    self._has_errors = True

            except ValueError:
                self._errors.append("Ongeldig datumformaat. Gebruik DD-MM-YYYY.")
                self._has_errors = True

    def validate(self):
        self._validate_address_type()
        self._validate_date_from()
        self._validate_date_to()

    def get_errors(self):
        return self._errors, self._has_errors
