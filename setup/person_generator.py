from faker import Faker
from setup.gemeente_loader import GemeenteLoader

class PersonGenerator:
    def __init__(self, gemeente_loader: GemeenteLoader):
        self.gemeente_loader = gemeente_loader
        self.fake = Faker('nl_BE')

    def generate_person(self):
        gemeente = self.gemeente_loader.get_random_gemeente()

        geboortedatum = self.fake.date_of_birth(minimum_age=1, maximum_age=90)
        geboortedatum_str = geboortedatum.strftime('%d-%m-%Y')

        # BRN opbouwen
        datum_str = geboortedatum.strftime('%y%m%d')  # bijv. 920316
        volgnummer = self.fake.random_int(min=1, max=997)
        volgnummer_str = f"{volgnummer:03d}"
        fake_control = self.fake.random_int(min=10, max=97)
        control_str = f"{fake_control:02d}"

        brn = f"{datum_str}-{volgnummer_str}-{control_str}"

        return {
            "voornaam": self.fake.first_name(),
            "achternaam": self.fake.last_name(),
            "geboortedatum": geboortedatum_str,
            "gemeente_id": gemeente['id'],
            "bevolkingsregisternummer": brn
        }