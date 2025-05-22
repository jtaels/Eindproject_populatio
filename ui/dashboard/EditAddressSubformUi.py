import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry

from controller.dashboard.EditAddressSubformController import EditAddressSubformController


class EditAddressSubformUi(tk.Toplevel):
    def __init__(self, master, person_address_id, app_controller, on_save):
        super().__init__(master)

        self.edit_address_subform_controller = EditAddressSubformController(person_address_id,self,app_controller.container)

        self.edit_address_subform_controller.on_save = on_save

        self.title("Adres bewerken")
        self.geometry("600x800")  # Ruim venster

        # Nieuw frame voor formulier
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(2, 2))

        # Layout instellingen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Adres soort
        ttk.Label(container, text="Adres soort").grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        addressTypeCombobox = ttk.Combobox(container, textvariable=self.edit_address_subform_controller.form["type"],state="readonly", width=30)
        addressTypeCombobox["values"] = [
            "Hoofdverblijfplaats",
            "Tijdelijk verblijf",
            "Instelling",
            "Verblijf bij familie / mantelzorg",
            "Vakantieverblijf / tweede verblijf",
            "Asielopvang / opvangcentrum"
        ]
        addressTypeCombobox.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Wonend sinds
        ttk.Label(container, text="Wonend sinds (dd-mm-yyyy)").grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        wonendEntry = DateEntry(container, width=20, dateformat='%d-%m-%Y')
        wonendEntry.entry.configure(textvariable=self.edit_address_subform_controller.form["from"])
        wonendEntry.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Verhuist op
        ttk.Label(container, text="Verhuist op (dd-mm-yyyy)").grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        verhuistEntry = DateEntry(container, width=20, dateformat='%d-%m-%Y')
        verhuistEntry.entry.configure(textvariable=self.edit_address_subform_controller.form["to"])
        verhuistEntry.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        # Actieknoppen onderaan
        self._build_action_buttons(container, row=6)

        # Zorg dat parent geblokkeerd wordt
        self.transient(master)
        self.grab_set()
        self.focus()
        self.wait_window(self)

    def _build_action_buttons(self, parent, row=6):
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, pady=(20, 20), sticky="e")

        # Toevoegen-knop
        toevoegen_button = ttk.Button(
            button_frame,
            text="Wijzigingen",
            command=self.edit_address_subform_controller.save_address
        )
        toevoegen_button.pack(side="right", padx=5)

        # Annuleren-knop
        annuleren_button = ttk.Button(
            button_frame,
            text="Annuleren",
            command=self.destroy
        )
        annuleren_button.pack(side="right", padx=5)
