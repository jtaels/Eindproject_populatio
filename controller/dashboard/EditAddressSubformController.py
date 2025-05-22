from db.entities.persoon import Persoon
from db.repositories.AdresRepository import AdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from db.repositories.PersoonRepository import PersoonRepository

import tkinter
from tkinter import messagebox

from validator.PersonAddressFormValidator import PersonAddressFormValidator

from applogging.Logger import  Logger

class EditAddressSubformController:

    def __init__(self, selected_address_id,master):

        self.selected_address_id = selected_address_id

        self.master = master
        self.on_save = None

        self.gemeente_repository = GemeenteRepository()
        self.address_repository = AdresRepository(self.gemeente_repository)
        self.person_repository = PersoonRepository(self.gemeente_repository)
        self.person_address_repository = PersoonAdresRepository(self.address_repository,self.person_repository)

        self.person_address = self.person_address_repository.find_by_id(self.selected_address_id)

        self.form = {

            "type": tkinter.StringVar(master,value=self.person_address.adres_type),
            "from":  tkinter.StringVar(master,value=self.person_address.van),
            "to":  tkinter.StringVar(master,value=self.person_address.tot)

        }

    def save_address(self):

        type = self.form['type'].get()
        afrom = self.form['from'].get()
        to = self.form['to'].get()

        validator = PersonAddressFormValidator(
            type,
            afrom,
            to
        )

        validator.validate()

        errors, has_errors = validator.get_errors()

        if has_errors:
            errorStr = ""
            for message in errors:
                errorStr += message + "\n"

            messagebox.showinfo("Controle", errorStr)
            return

        rows_updated = self.person_address_repository.update(self.selected_address_id,type,afrom,to)

        if rows_updated == 0:
            messagebox.showerror("Fout", "Kon de persoon niet wijzigen!")
            return

        messagebox.showinfo("Controle", "De adresgegevens werden gewijzigd!")

        Logger.info(f"Adresgegevens voor {self.selected_address_id} zijn bijgewerkt!")

        if self.on_save:
            self.on_save()

        self.master.destroy()
