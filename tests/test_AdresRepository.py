import unittest
import sqlite3
from db.repositories.AdresRepository import AdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.entities.adres import Adres
from db.entities.gemeente import Gemeente
from exceptions.AdresNotFound import AdresNotFoundException


class TestAdresRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Eenmalige setup voor de testklasse."""
        cls.gemeente_repo = GemeenteRepository()
        cls.adres_repo = AdresRepository(cls.gemeente_repo)

        # Testgemeente aanmaken
        cls.test_gemeente = cls.gemeente_repo.create(Gemeente("9999", "Ham", "3914", "Limburg"))

    @classmethod
    def tearDownClass(cls):
        """Opruiming na alle tests."""
        cls.gemeente_repo.delete(cls.test_gemeente.id)

    def setUp(self):
        """Voor elke test: een testadres aanmaken."""
        self.test_adres = self.adres_repo.create(Adres(0,"Teststraat", "123", "A", self.test_gemeente,[]))

    def tearDown(self):
        """Na elke test: het testadres verwijderen."""
        self.adres_repo.delete(self.test_adres.id)

    def test_create(self):
        """Test of een adres correct wordt aangemaakt."""
        adres = Adres(0,"Nieuwstraat", "5", None, self.test_gemeente, [])
        saved_adres = self.adres_repo.create(adres)

        self.assertIsNotNone(saved_adres.id)
        self.assertEqual(saved_adres.straatnaam, "Nieuwstraat")

        # Cleanup
        self.adres_repo.delete(saved_adres.id)

    def test_find_by_id(self):
        """Test of een adres correct wordt opgehaald op ID."""
        adres = self.adres_repo.find_by_id(self.test_adres.id)
        self.assertEqual(adres.id, self.test_adres.id)

    def test_find(self):
        """Test of een adres correct wordt gevonden."""
        adressen = self.adres_repo.find("Teststraat", "123", "A", self.test_gemeente)
        self.assertGreater(len(adressen), 0)
        self.assertEqual(adressen[0].straatnaam, "Teststraat")

    def test_find_all_by_gemeente(self):
        """Test of alle adressen in een gemeente worden opgehaald."""
        adressen = self.adres_repo.find_all_by_gemeente(self.test_gemeente)
        self.assertGreater(len(adressen), 0)

    def test_delete(self):
        """Test of een adres correct wordt verwijderd."""
        adres = self.adres_repo.create(Adres(0, "Nieuwstraat", "1", None, self.test_gemeente, []))
        rows_deleted = self.adres_repo.delete(adres.id)
        self.assertEqual(rows_deleted, 1)

        with self.assertRaises(AdresNotFoundException):
            self.adres_repo.find_by_id(adres.id)


if __name__ == "__main__":
    unittest.main()
