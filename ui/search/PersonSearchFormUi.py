import tkinter as tk
from tkinter import ttk

from controller.search.PersonSearchController import PersonSearchController
from services.PersoonService import PersoonService


class PersonSearchFormUi:

    def __init__(self, parent_element,app_controller, on_submit=None,):

        self._person_search_controller = PersonSearchController(app_controller)
        self._parent_element = parent_element

        self._person_search_controller.on_submit = on_submit

    def build(self):

        self.search_frame = ttk.Labelframe(self._parent_element, text="Zoeken")

        self.search_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.search_frame, text="Voornaam").grid(row=0, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(self.search_frame, width=30, textvariable=self._person_search_controller.search_form['firstname']).grid(
            row=1, column=0, padx=20, pady=5, sticky="ew"
        )

        ttk.Label(self.search_frame, text="Achternaam").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(self.search_frame, width=30, textvariable=self._person_search_controller.search_form['lastname']).grid(
            row=3, column=0, padx=20, pady=5, sticky="ew"
        )

        ttk.Label(self.search_frame, text="Bevolkingsregisternr").grid(row=4, column=0, padx=20, pady=(5, 0),
                                                                       sticky="w")
        ttk.Entry(self.search_frame, width=30,
                  textvariable=self._person_search_controller.search_form['bevolkingsregisternummer']).grid(
            row=5, column=0, padx=20, pady=5, sticky="ew"
        )

        ttk.Button(self.search_frame, text="Zoeken", command=self._person_search_controller.search_person,
                       bootstyle="success").grid(
                row=6, column=0, pady=5, padx=20, sticky="ew"
        )

        return self.search_frame

    def getController(self) -> PersonSearchController:

        return self._person_search_controller