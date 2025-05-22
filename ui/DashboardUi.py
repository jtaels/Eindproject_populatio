import tkinter as tk
from tkinter import ttk
from ttkbootstrap import ttk
from ttkbootstrap.widgets import DateEntry

from ui.dashboard.AddressUi import AddressUi
from ui.dashboard.LoggingUi import LoggingUi
from ui.dashboard.PersonDetailsUi import PersonDetailsUi


class DashboardUi:

    def __init__(self, controller, main_frame):
        self._controller = controller
        self._root = main_frame

        self._build_tabs()

        self._placeholder_text = "../../...."

    def _build_tabs(self):

        #Noteboek voor navigatie aanmaken
        notebook = ttk.Notebook(self._root)
        notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Tabladen toevoegen
        tab_person = ttk.Frame(notebook)
        tab_address = ttk.Frame(notebook)
        tab_logs = ttk.Frame(notebook)

        notebook.add(tab_person, text="Persoonsysteem")
        notebook.add(tab_address, text="Adressen")

        #Enkel administrators kunnen de logs inkijken
        if self._controller.get_app_controller().get_user().role == 100:
            notebook.add(tab_logs, text="Logs")

        #Nieuwe instance aanmaken van  de persondetails menu. Vervolgens deze klasse opbouwen zodat de layout verschijnt
        person_details_ui = PersonDetailsUi(self._controller, tab_person)
        person_details_ui.build()

        address_ui = AddressUi(self._controller,tab_address)
        address_ui.build()

        loggin_ui = LoggingUi(self._controller,tab_logs)
        loggin_ui.build()