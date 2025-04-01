import tkinter as tk
from tkinter import ttk
from ttkbootstrap import ttk
from ttkbootstrap.widgets import DateEntry

class PersonDetailsUi:

    def __init__(self, dashboard_controller, tab_person):

        self._dashboard_controller = dashboard_controller
        self._tab_person = tab_person


    def _build_top_section(self):
        top_frame = ttk.Frame(self._tab_person)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Zorgt ervoor dat de bovenste sectie meebeweegt
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)

        # Zoekformulier
        search_frame = ttk.Labelframe(top_frame, text="Zoeken")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Laat de rijen netjes verdelen
        for i in range(7):
            search_frame.grid_rowconfigure(i, weight=1)
        search_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(search_frame, text="Voornaam").grid(row=0, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(search_frame, width=30, textvariable=self._dashboard_controller.search_form['firstname']).grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Achternaam").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(search_frame, width=30, textvariable=self._dashboard_controller.search_form['lastname']).grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Bevolkingsregisternr").grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(search_frame, width=30, textvariable=self._dashboard_controller.search_form['bevolkingsregisternummer']).grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        search_btn_last_row = 6
        for action in self._dashboard_controller.get_search_form_actions():
            ttk.Button(search_frame, text=action['name'], bootstyle=action['style'], command=action['command']).grid(row=search_btn_last_row, column=0, pady=5, padx=20, sticky="ew")
            search_btn_last_row += 1

        self._build_person_fiche_form(top_frame)

    def _build_person_fiche_form(self,top_frame):
        # Persoonsdataformulier
        data_frame = ttk.Labelframe(top_frame, text="Persoonsdata")
        data_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Laat de rijen netjes verdelen
        for i in range(10):
            data_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            data_frame.grid_columnconfigure(j, weight=1)

        ttk.Label(data_frame, text="Bevolkingsregisternr").grid(row=0, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=30, state='disabled', textvariable=self._dashboard_controller.person_fiche['bevolkingsregisternr']).grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Voornaam").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=20, textvariable=self._dashboard_controller.person_fiche['voornaam']).grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Achternaam").grid(row=2, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=20, textvariable=self._dashboard_controller.person_fiche['achternaam']).grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Geboortedatum (dd-mm-yyyy)").grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        birthdateEntry = DateEntry(data_frame, width=20, dateformat='%d-%m-%Y')
        birthdateEntry.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        birthdateEntry.entry.configure(textvariable=self._dashboard_controller.person_fiche['geboortedatum'])

        ttk.Label(data_frame, text="Geboorteplaats").grid(row=4, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Combobox(data_frame, width=20, textvariable=self._dashboard_controller.person_fiche['geboorteplaats']).grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Overlijdensdatum (dd-mm-yyyy)").grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        deathdateEntry = DateEntry(data_frame, width=20, dateformat='%d-%m-%Y')
        deathdateEntry.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        deathdateEntry.entry.configure(textvariable=self._dashboard_controller.person_fiche['overlijdensdatum'])

        ttk.Label(data_frame, text="Overlijdensplaats").grid(row=6, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Combobox(data_frame, width=20, textvariable=self._dashboard_controller.person_fiche['overlijdensplaats']).grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Overlijdensoorzaak").grid(row=8, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=50, textvariable=self._dashboard_controller.person_fiche['overlijdenoorzaak']).grid(row=9, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        fiche_btn_last_row = 10
        for action in self._dashboard_controller.get_fiche_form_actions():
            ttk.Button(data_frame, text=action['name'], bootstyle=action['style'], command=action['command']).grid(row=fiche_btn_last_row, columnspan=2, pady=5, padx=20, sticky="ew")
            fiche_btn_last_row += 1

    def _build_tree_view(self):
        tree_frame = ttk.Frame(self._tab_person)
        tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self._tab_person.grid_rowconfigure(1, weight=1)

        ttk.Label(tree_frame, text="Persoonlijst").grid(row=0, column=0, pady=5, sticky="w")

        columns = ("Straat", "Huisnummer", "Busnummer", "Postcode", "Gemeente", "Provincie", "Achternaam", "Voornaam", "Van", "Tot")
        self._dashboard_controller.result_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self._dashboard_controller.result_tree.heading(col, text=col)
            self._dashboard_controller.result_tree.column(col, width=100, anchor="center")

        self._dashboard_controller.result_tree.grid(row=1, column=0, pady=5, sticky="nsew")
        self._dashboard_controller.result_tree.bind("<ButtonRelease-1>", self._dashboard_controller.on_tree_item_click)

        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)


    def build(self):

        #Bouw de person detailsui op
        self._build_top_section()
        self._build_tree_view()

