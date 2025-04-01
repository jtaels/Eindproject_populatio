from tkinter import StringVar

from pyexpat.errors import messages

from db.entities.gemeente import Gemeente
from db.entities.persoon import Persoon
from db.repositories.AdresRepository import AdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from db.repositories.PersoonRepository import PersoonRepository
import tkinter
from tkinter import messagebox

from exceptions.AdresNotFound import AdresNotFoundException
from exceptions.FormErrorException import FormErrorException
from exceptions.PersonUpdateFailure import PersonUpdateFailureException
from manager.GemeenteManager import GemeenteManager
from services.AdresService import AdresService
from services.GemeenteService import GemeenteService
from services.PersoonService import PersoonService
from datetime import date
from datetime import datetime


class DashboardController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        gemeente_repository = GemeenteRepository()
        persoon_repository = PersoonRepository(gemeente_repository)
        address_repository = AdresRepository(gemeente_repository)
        person_address_repository = PersoonAdresRepository(address_repository,persoon_repository)

        self._persoon_service = PersoonService(persoon_repository)
        self._gemeente_service = GemeenteService(gemeente_repository)
        self._gemeente_manager = GemeenteManager(self._gemeente_service)
        self._address_service = AdresService(address_repository, person_address_repository)
        self._persons = []
        self.gemeenten_namen = list(self._gemeente_manager.gemeente_dict.keys())

        self._init_forms()

        self._init_person_fiche()

        self.result_tree = None

    def _init_forms(self):

        self.search_form = {

            "firstname": tkinter.StringVar(),
            "lastname": tkinter.StringVar(),
            "bevolkingsregisternummer": tkinter.StringVar()


        }

        self.address_search_from = {

            "street": tkinter.StringVar(),
            "huisnummer": tkinter.StringVar(),
            "busnummer": tkinter.StringVar(),
            "postcode": tkinter.StringVar(),
            "gemeente": tkinter.StringVar()

        }

        #Wanneer een gebruiker invoer doet in de postcode moeten we gaan kijken welke gemeente erbij hoort
        self.address_search_from['postcode'].trace("w", self.on_postcode_change)

    def on_postcode_change(self, *args):

        entry_value = self.address_search_from['postcode'].get()

        #Bij nieuwe invoer het veld telkens leeg maken
        self.address_search_from['gemeente'].set("")

        #Postcodes in belgie bevatten 4 nummers daarom pas vanaf 4 karakters de bijhorende gemeente gaan zoeken
        if len(entry_value) >= 4:

            gemeente = self._gemeente_manager.get_gemeente_by_postcode(entry_value)

            if gemeente:
                self.address_search_from['gemeente'].set(gemeente.naam)

    def on_gemeente_change(self, event):

        entry_value = self.address_search_from['gemeente'].get()

        #Bij nieuwe invoer het veld telkens leeg maken
        self.address_search_from['postcode'].set("")

        gemeente = self._gemeente_manager.get_gemeente_by_name(entry_value)

        if gemeente:
            self.address_search_from['postcode'].set(gemeente.postcode)

    def _init_person_fiche(self) -> None:

        self.person_fiche = {

            'entity': None,
            'bevolkingsregisternr': StringVar(),
            'voornaam': StringVar(),
            'achternaam': StringVar(),
            'geboortedatum': StringVar(),
            'geboorteplaats': StringVar(),
            'overlijdensdatum': StringVar(),
            'overlijdensplaats': StringVar(),
            'overlijdenoorzaak': StringVar(),
            'addresses': []

        }

    def _fill_person_fiche(self,person:Persoon):

        self._clear_person_fiche()

        geboorteplaats = "" if person.geboorteplaats is None else person.geboorteplaats.naam
        geboortedatum = "" if person.geboortedatum is None else person.geboortedatum.strftime("%d-%m-%Y")
        overlijdensplaats = "" if person.overlijdensplaats is None else person.overlijdensplaats.naam
        overlijdensdatum = "" if person.overlijdensdatum is None else person.overlijdensdatum.strftime("%d-%m-%Y")
        overlijdensoorzaak = "" if person.overlijdensoorzaak is None else person.overlijdensoorzaak

        self.person_fiche['entity'] = person
        self.person_fiche['bevolkingsregisternr'].set(person.bevolkingsregisternummer)
        self.person_fiche['voornaam'].set(person.voornaam)
        self.person_fiche['achternaam'].set(person.achternaam)
        self.person_fiche['geboortedatum'].set(geboortedatum)
        self.person_fiche['geboorteplaats'].set(geboorteplaats)
        self.person_fiche['overlijdensdatum'].set(overlijdensdatum)
        self.person_fiche['overlijdensplaats'].set(overlijdensplaats)
        self.person_fiche['overlijdenoorzaak'].set(overlijdensoorzaak)
        self.person_fiche['addresses'] = person.adressen

    def _clear_person_fiche(self):

        self.person_fiche['bevolkingsregisternr'].set("")
        self.person_fiche['voornaam'].set("")
        self.person_fiche['achternaam'].set("")
        self.person_fiche['geboortedatum'].set("")
        self.person_fiche['geboorteplaats'].set("")
        self.person_fiche['overlijdensdatum'].set("")
        self.person_fiche['overlijdensplaats'].set("")
        self.person_fiche['overlijdenoorzaak'].set("")
        self.person_fiche['addresses'] = []


    def _search_person(self):

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

        self._fill_tree(results)

    def _search_address(self):

        '''
                    "street": tkinter.StringVar(),
            "huisnummer": tkinter.StringVar(),
            "busnummer": tkinter.StringVar(),
            "postcode": tkinter.StringVar(),
            "gemeente": tkinter.StringVar()
        :return:
        '''

        straat_var = self.address_search_from['street'].get()
        huisnummer_var = self.address_search_from['huisnummer'].get()
        busnummer_var = self.address_search_from['busnummer'].get()
        postcode_var = self.address_search_from['postcode'].get()
        gemeente_var = self.address_search_from['gemeente'].get()

        if not straat_var or not huisnummer_var or not postcode_var or not gemeente_var:
            messagebox.showinfo("Controle", "Volgende velden zijn verplicht: straat, huisnummer, postcode, gemeente")
            return

        gemeente = self._gemeente_manager.get_gemeente_by_name(gemeente_var)

        #Busnummer mag leeg zijn in dat geval bedoeld de gebruiker busnummer A
        if not busnummer_var:
            busnummer_var = self.address_search_from['busnummer'].set("A")

        if not gemeente:
            messagebox.showinfo("Controle", "Dit is geen gemeente in het Koninkrijk België")
            return

        try:

            address = self._address_service.find_one(straat_var,huisnummer_var,busnummer_var,gemeente)

            print(address)

        except AdresNotFoundException:
            messagebox.showinfo("Controle", "We kunnen het opgegeven adres niet vinden. Controleer of de straatnaam, huisnummer, postcode en stad juist zijn ingevoerd.")

    def _fill_tree(self, results):

        data = []

        self._clear_tree()

        for result in results:

            #Alle adressen doorlopen
            adresses = result.adressen

            achternaam = result.achternaam,
            voornaam =  result.voornaam

            #persoonAdres entity
            for address in adresses:

                straat = address.adres.straatnaam
                huisnummer = address.adres.huisnummer
                busnummer = address.adres.busnummer
                postcode = address.adres.gemeente.postcode
                gemeente = address.adres.gemeente.naam
                provincie = address.adres.gemeente.provincie
                van = address.van,
                tot = address.tot

                self.result_tree.insert("", "end",values=(straat,huisnummer,busnummer,postcode,gemeente,provincie,achternaam,voornaam,van,tot),tags=[result.id,])

    def _clear_tree(self) -> None:

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def on_tree_item_click(self, event) -> None:

        item = self.result_tree.focus()
        item_data = self.result_tree.item(item)
        tags = item_data['tags']

        if(len(tags) == 0):
            messagebox.showerror("Fout!", "Het aangeklikte item bevat een fout!")
            return

        user_id = tags[0]
        user = self._find_in_founded_persons(user_id)

        self._fill_person_fiche(user)

    def _find_in_founded_persons(self, user_id) -> object:

        for person in self._persons:

            if person.id == user_id:
                return person

    def get_search_form_actions(self) -> list:

        actions = []

        actions.append(self._build_action_obj('Zoeken', 'success', self._search_person))

        if self._app_controller.get_user().role == 100:

            actions.append(self._build_action_obj('Gemeenten beheren', 'default', None))

        actions.append(self._build_action_obj('Zoeken op adres', 'default', None))

        return actions

    def get_address_search_form_actions(self) -> list:

        actions = []

        actions.append(self._build_action_obj('Zoeken', 'success', self._search_address))

        return actions

    def _update_person(self) -> None:

        person = self.person_fiche['entity']

        if not person:
            messagebox.showinfo("info", "Je moet eerst een persoon selecteren!")
            return

        geboorteplaats = self._gemeente_manager.get_gemeente_by_name(self.person_fiche['geboorteplaats'].get())

        if not geboorteplaats:
            messagebox.showinfo("Info","Je moet een geboorteplaats uit de lijst kiezen!")
            return

        if self.person_fiche['overlijdensplaats'].get().strip():
            overlijdensplaats = self._gemeente_manager.get_gemeente_by_name(self.person_fiche['overlijdensplaats'].get())

            if not overlijdensplaats:
                messagebox.showinfo("Info", "Je moet een overlijdensplaats uit de lijst kiezen!")
                return

            person.overlijdensplaats = overlijdensplaats

        geboortedatum = datetime.strptime(self.person_fiche['geboortedatum'].get(),"%d-%m-%Y") if self.person_fiche['geboortedatum'].get() else None
        overlijdensdatum = datetime.strptime(self.person_fiche['overlijdensdatum'].get(),"%d-%m-%Y") if self.person_fiche['overlijdensdatum'].get() else None

        person.voornaam = self.person_fiche['voornaam'].get()
        person.achternaam = self.person_fiche['achternaam'].get()
        person.geboortedatum = geboortedatum
        person.geboorteplaats = geboorteplaats
        person.overlijdensdatum = overlijdensdatum
        person.overlijdenoorzaak = self.person_fiche['overlijdenoorzaak'].get()

        try:

            self._persoon_service.update_persoon(person)
        except PersonUpdateFailureException as e:
            messagebox.showerror("Fout!", "Er ging iets mis bij het bewerken van deze persoon!")
            return
        except FormErrorException as e:
            errorStr = ""
            for message in e.messages:
                errorStr += message + "\n"

            messagebox.showinfo("Controle", errorStr)
            return

        messagebox.showinfo("Controle", "De persoon is gewijzigd!")


    def get_fiche_form_actions(self) -> list:

        actions = []

        if self._app_controller.get_user().role > 50:

            actions.append(self._build_action_obj('Wijzigen', 'success', self._update_person))

        if self._app_controller.get_user().role == 100:
            actions.append(self._build_action_obj('Verwijderen', 'danger', None))

        return actions

    def _build_action_obj(self, name:str,style:str, command) -> object:

        return {

            'name': name,
            'style': style,
            'command': command

            }