import tkinter

from db.repositories.GemeenteRepository import GemeenteRepository
from db.repositories.PersoonRepository import PersoonRepository
from services.PersoonService import PersoonService
from tkinter import messagebox

class PersonSearchController:

    def __init__(self, app_controller):

        gemeente_repository = GemeenteRepository()
        persoon_repository = PersoonRepository(gemeente_repository)
        persoon_service = PersoonService(persoon_repository)

        self._persoon_service = persoon_service
        self._app_controller = app_controller
        self.on_submit = None
        self._persons = []

        self.search_form = {

            "firstname": tkinter.StringVar(),
            "lastname": tkinter.StringVar(),
            "bevolkingsregisternummer": tkinter.StringVar()


        }

    def search_person(self) -> None:

        firstname = self.search_form['firstname'].get()
        lastname = self.search_form['lastname'].get()
        bevolkingsregisternummer = self.search_form['bevolkingsregisternummer'].get()

        #Als er op bevolkingsnummer moet gezocht worden niet kijken naar de voornaam achternaam
        if bevolkingsregisternummer:
            pass

        if len(firstname) < 2 or len(lastname) < 3:
            messagebox.showinfo("info", "Voornaam en achternaam verplicht!")
            return

        results = self._persoon_service.search_by_name(firstname,lastname)

        if(len(results) == 0):
            messagebox.showinfo("Info", "Er zijn geen resultaten gevonden voor deze zoekopdracht!")

        self._persons = results

        if self.on_submit:
            self.on_submit(results)

    def find_in_founded_persons(self, user_id) -> object:

        for person in self._persons:

            if person.id == user_id:
                return person