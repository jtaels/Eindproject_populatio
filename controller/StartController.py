import ui.SignInUi as signInUi
import controller.SignInController as signInController
import tkinter

from db.entities.adres import Adres
from db.repositories.AdresRepository import AdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from db.repositories.PersoonRepository import PersoonRepository
from exceptions.PersonNotFound import PersonNotFoundException
from generator.AdresHistoriekPdfGenerator import AdresHistoriekPdfGenerator
from services.AdresService import AdresService
from services.PersoonService import PersoonService

from tkinter import messagebox
from tkinter import filedialog
import os

class StartController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        self._gemeente_repository = GemeenteRepository()
        self._adres_repository = AdresRepository(self._gemeente_repository)
        self._person_repository = PersoonRepository(self._gemeente_repository)
        self._person_address_repository = PersoonAdresRepository(self._adres_repository,self._person_repository)
        self._person_service = PersoonService(self._person_repository)
        self._adres_service = AdresService(self._adres_repository,self._person_address_repository)

    '''

        Gebruiker doet aanvraag om gezinssamenstelling en adreshistoriek op te vragen

    '''
    def handle_request_adreshistoriek(self, bevolkingsregisternummer:str):

        try:

            person = self._person_service.get_person_by_bevolkingsregisternr(bevolkingsregisternummer)

            addresses = self._adres_service.get_by_person(person)

            persoon_naam = person.voornaam + " " + person.achternaam
            file_name =f"{persoon_naam}_adres_historiek.pdf"

            adres_historiek_pdf_gen = AdresHistoriekPdfGenerator(persoon_naam)

            adres_historiek_pdf_gen.set_addresses(addresses)

            to_save_path = self.set_save_path(file_name)

            adres_historiek_pdf_gen.generate(to_save_path)

            open_file = messagebox.askyesno("Actie", "Wil je dit bestand nu openen?")

            if open_file:
                os.startfile(to_save_path)

        except PersonNotFoundException as e:
            messagebox.showinfo("Info", "Deze persoon bestaat niet!")
        except FileNotFoundError as e:
            messagebox.showwarning("Info", "Het opgegeven path kan niet worden gevonden")

    def set_save_path(self,default_file_name:str) -> str:

        file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=default_file_name
         )

        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            raise FileNotFoundError

        return file_path

    def open_sign_in_screen(self,main_frame):

        self._app_controller.switch_screen('signIn', main_frame)