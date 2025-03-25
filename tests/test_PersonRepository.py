import unittest
from unittest.mock import MagicMock
import random
from datetime import datetime
from db.repositories.AdresRepository import AdresRepository
from db.repositories.PersoonRepository import PersoonRepository
from exceptions.PersonCreateFailure import PersonCreateFailureException
from exceptions.PersonNotFound import PersonNotFoundException
from db.entities.persoon import Persoon  #

class TestPersoonRepository(unittest.TestCase):
    def setUp(self):
        # Maak een mock database-verbinding en repository
        self.mock_db = MagicMock()

        self.repository = PersoonRepository(self.mock_db)  # Pas aan naar jouw repository naam

    def generate_mock_bevolkingsnummer(self):
        # Willekeurige geboortedatum tussen 1 januari 1900 en 31 december 2020
        birth_date = datetime(random.randint(1900, 2020), random.randint(1, 12), random.randint(1, 28))

        # Deel 1: geboortedatum in DDMMJJ formaat
        geboortedatum = birth_date.strftime("%d%m%y")

        # Deel 2: willekeurig volgnummer tussen 000 en 999
        volgnummer = f"{random.randint(0, 999):03}"

        # Deel 3: willekeurig controlegetal tussen 00 en 99
        controlegetal = f"{random.randint(0, 99):02}"

        # Gecombineerd bevolkingsnummer
        bevolkingsnummer = f"{geboortedatum}-{volgnummer}-{controlegetal}"

        return bevolkingsnummer

    def test_find_by_name(self):
        # Stel mock resultaten in voor de fetch_all methode van de database
        mock_results = [
            (1, "Jan", "Peeters", "1980-06-15", 1, None, None, None, "BE123456789"),
            (2, "Maria", "Peeters", "1985-09-21", 2, "2022-04-10", 1, "Natuurlijke oorzaak", "BE987654321")
        ]
        self.mock_db.fetch_all.return_value = mock_results

        # Stel de _build_entity en _fill_adresses methodes in, zodat we de juiste persoon objecten krijgen
        persoon_1 = Persoon(1, "Jan", "Peeters", "1980-06-15", None, None, None, None, "BE123456789")
        persoon_2 = Persoon(2, "Maria", "Peeters", "1985-09-21", None, "2022-04-10", None, "Natuurlijke oorzaak",
                            "BE987654321")
        self.repository._build_entity = MagicMock(side_effect=[persoon_1, persoon_2])
        self.repository._fill_adresses = MagicMock()

        # Roep de functie aan
        result = self.repository.find_by_name("", "Peeters")  # Zoeken naar "Jan" en "Peeters"

        # Controleer of het juiste aantal personen wordt teruggegeven
        self.assertEqual(len(result), 2)  # Aangezien beide "Jan" en "Maria" worden geretourneerd

        # Controleer of de _build_entity methode correct werd aangeroepen met de juiste waarden (de tuple)
        self.repository._build_entity.assert_any_call(
            (1, "Jan", "Peeters", "1980-06-15", 1, None, None, None, "BE123456789")
        )
        self.repository._build_entity.assert_any_call(
            (2, "Maria", "Peeters", "1985-09-21", 2, "2022-04-10", 1, "Natuurlijke oorzaak", "BE987654321")
        )

        # Controleer of de _fill_adresses method voor beide personen werd aangeroepen
        self.repository._fill_adresses.assert_any_call(persoon_1)
        self.repository._fill_adresses.assert_any_call(persoon_2)

        # Controleer of de personen de juiste waarden hebben
        self.assertEqual(result[0].voornaam, "Jan")
        self.assertEqual(result[0].achternaam, "Peeters")
        self.assertEqual(result[1].voornaam, "Maria")
        self.assertEqual(result[1].achternaam, "Peeters")

    def test_find_by_id_person_found(self):
        # Stel in wat de mock database zal retourneren
        mock_data = {
            'id': 1,
            'voornaam': 'Jan',
            'achternaam': 'Peeters',
            'geboortedatum': '1990-01-01',
            'geboorteplaats_id': 1,
            'overlijdensdatum': None,
            'overlijdensplaats_id': None,
            'overlijdensoorzaak': None,
            'bevolkingsregisternummer': None
        }

        # Stel in dat fetch_one de mock data retourneert
        self.mock_db.fetch_one.return_value = mock_data

        # Voer de test uit
        persoon = self.repository.find_by_id(1)

        # Test of de repository een instantie van Persoon retourneert
        self.assertIsInstance(persoon, Persoon)
        self.assertEqual(persoon.voornaam, 'Jan')
        self.assertEqual(persoon.achternaam, 'Geyskens')

    def test_find_by_id_person_not_found(self):
        # Stel in dat fetch_one geen resultaat retourneert (None)
        self.mock_db.fetch_one.return_value = None

        # Verwacht dat er een exception wordt opgegooid
        with self.assertRaises(PersonNotFoundException):
            self.repository.find_by_id(999)  # Dit id bestaat niet

    def test_create_person_success(self):
        # Maak een mock Persoon object
        persoon = Persoon(
            id=None,  # id wordt nog niet toegewezen
            voornaam="Hans",
            achternaam="Bergen",
            geboortedatum="1985-10-12",
            geboorteplaats=None,
            overlijdensdatum=None,
            overlijdensplaats=None,
            overlijdensoorzaak=None,
            bevolkingsregisternummer=self.generate_mock_bevolkingsnummer()
        )

        # Mock de insert methode van de database om een succesvolle insert te simuleren
        self.mock_db.insert.return_value = 1  # Simuleer een succesvol resultaat met een ID van 1

        # Voer de functie uit
        result = self.repository.create_person(persoon)

        # Controleer of het ID van de persoon correct is ingesteld
        self.assertEqual(result.id, 1)
        self.assertEqual(result.voornaam, "Jan")
        self.assertEqual(result.achternaam, "Peeters")

    def test_create_person_failure(self):
        # Maak een mock Persoon object
        persoon = Persoon(
            id=None,  # id wordt nog niet toegewezen
            voornaam="Jan",
            achternaam="Peeters",
            geboortedatum="1985-10-12",
            geboorteplaats=None,
            overlijdensdatum=None,
            overlijdensplaats=None,
            overlijdensoorzaak=None,
            bevolkingsregisternummer=self.generate_mock_bevolkingsnummer()
        )

        # Mock de insert methode van de database om een mislukte insert te simuleren
        self.mock_db.insert.return_value = 0  # Simuleer een mislukte insert (ID is 0)

        # Test of de uitzondering wordt opgegooid
        with self.assertRaises(PersonCreateFailureException):
            self.repository.create_person(persoon)

if __name__ == "__main__":
    unittest.main()
