import tkinter as tk
from tkinter import ttk
from ttkbootstrap import ttk
from ttkbootstrap.widgets import DateEntry

class DashboardUi:

    def __init__(self, controller, main_frame):
        self._controller = controller
        self._root = main_frame

        self._build_tabs()

        self._placeholder_text = "../../...."

    def _build_tabs(self):
        # Maak het notebook aan (tabsysteem)
        notebook = ttk.Notebook(self._root)
        notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Voeg tabbladen toe
        tab_person = ttk.Frame(notebook)
        tab_address = ttk.Frame(notebook)

        notebook.add(tab_person, text="Persoonsysteem")
        notebook.add(tab_address, text="Adressen")

        # Vul de tabbladen met de juiste secties
        self._build_top_section(tab_person)
        self._build_tree_view(tab_person)  # Treeview blijft bij Persoonsysteem
        self._build_address_view(tab_address)  # Adressen wordt in het tabblad "Adressen" gezet

    def _build_top_section(self, tab_person):
        top_frame = ttk.Frame(tab_person)
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
        ttk.Entry(search_frame, width=30, textvariable=self._controller.search_form['firstname']).grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Achternaam").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(search_frame, width=30, textvariable=self._controller.search_form['lastname']).grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(search_frame, text="Bevolkingsregisternr").grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(search_frame, width=30, textvariable=self._controller.search_form['bevolkingsregisternummer']).grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        search_btn_last_row = 6
        for action in self._controller.get_search_form_actions():
            ttk.Button(search_frame, text=action['name'], bootstyle=action['style'], command=action['command']).grid(row=search_btn_last_row, column=0, pady=5, padx=20, sticky="ew")
            search_btn_last_row += 1

        self._build_person_fiche_form(top_frame)

    def _build_person_fiche_form(self, top_frame):
        # Persoonsdataformulier
        data_frame = ttk.Labelframe(top_frame, text="Persoonsdata")
        data_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Laat de rijen netjes verdelen
        for i in range(10):
            data_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            data_frame.grid_columnconfigure(j, weight=1)

        ttk.Label(data_frame, text="Bevolkingsregisternr").grid(row=0, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=30, state='disabled', textvariable=self._controller.person_fiche['bevolkingsregisternr']).grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Voornaam").grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=20, textvariable=self._controller.person_fiche['voornaam']).grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Achternaam").grid(row=2, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=20, textvariable=self._controller.person_fiche['achternaam']).grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Geboortedatum (dd-mm-yyyy)").grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        birthdateEntry = DateEntry(data_frame, width=20, dateformat='%d-%m-%Y')
        birthdateEntry.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        birthdateEntry.entry.configure(textvariable=self._controller.person_fiche['geboortedatum'])

        ttk.Label(data_frame, text="Geboorteplaats").grid(row=4, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Combobox(data_frame, width=20, textvariable=self._controller.person_fiche['geboorteplaats']).grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Overlijdensdatum (dd-mm-yyyy)").grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        deathdateEntry = DateEntry(data_frame, width=20, dateformat='%d-%m-%Y')
        deathdateEntry.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        deathdateEntry.entry.configure(textvariable=self._controller.person_fiche['overlijdensdatum'])

        ttk.Label(data_frame, text="Overlijdensplaats").grid(row=6, column=1, padx=20, pady=(5, 0), sticky="w")
        ttk.Combobox(data_frame, width=20, textvariable=self._controller.person_fiche['overlijdensplaats']).grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        ttk.Label(data_frame, text="Overlijdensoorzaak").grid(row=8, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="w")
        ttk.Entry(data_frame, width=50, textvariable=self._controller.person_fiche['overlijdenoorzaak']).grid(row=9, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        fiche_btn_last_row = 10
        for action in self._controller.get_fiche_form_actions():
            ttk.Button(data_frame, text=action['name'], bootstyle=action['style'], command=action['command']).grid(row=fiche_btn_last_row, columnspan=2, pady=5, padx=20, sticky="ew")
            fiche_btn_last_row += 1

    def _build_tree_view(self, tab_person):
        tree_frame = ttk.Frame(tab_person)
        tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Zorgt ervoor dat tree_frame mee schaalt
        tab_person.grid_rowconfigure(1, weight=1)

        ttk.Label(tree_frame, text="Persoonlijst").grid(row=0, column=0, pady=5, sticky="w")

        columns = ("Straat", "Huisnummer", "Busnummer", "Postcode", "Gemeente", "Provincie", "Achternaam", "Voornaam", "Van", "Tot")
        self._controller.result_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self._controller.result_tree.heading(col, text=col)
            self._controller.result_tree.column(col, width=100, anchor="center")

        self._controller.result_tree.grid(row=1, column=0, pady=5, sticky="nsew")
        self._controller.result_tree.bind("<ButtonRelease-1>", self._controller.on_tree_item_click)

        # Zorgt ervoor dat de treeview mee schaalt
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def _build_address_view(self, tab_address):
        # Dit is een lege placeholder voor het adres tabblad, kan verder worden ingevuld.
        ttk.Label(tab_address, text="Adreslijst").grid(row=0, column=0, pady=5, sticky="w")
        # Hier kun je de benodigde code voor adressen toevoegen, bijvoorbeeld een Treeview voor adressen.
