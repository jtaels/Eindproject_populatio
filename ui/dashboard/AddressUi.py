import tkinter as tk
from tkinter import ttk
from ttkbootstrap import ttk
from ttkbootstrap.widgets import DateEntry

class AddressUi:

    def __init__(self, dashboard_controller, tab_address):

        self._dashboard_controller = dashboard_controller
        self._tab_address = tab_address


    def _build_top_section(self):
        top_frame = ttk.Frame(self._tab_address)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Zorgt ervoor dat de bovenste sectie meebeweegt
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)

        # Zoekformulier
        search_frame = ttk.Labelframe(top_frame, text="Zoeken")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        search_frame.columnconfigure(0, weight=2)  # Straatnaam
        search_frame.columnconfigure(1, weight=1)  # Huisnummer
        search_frame.columnconfigure(2, weight=1)  # Busnummer
        search_frame.columnconfigure(3, weight=1)  # Postcode
        search_frame.columnconfigure(4, weight=2)  # Gemeente

        ttk.Label(search_frame, text="Straatnaam:").grid(row=0, column=0, sticky="w", pady=(5, 2))
        ttk.Label(search_frame, text="Huisnr:").grid(row=0, column=1, sticky="w", pady=(5, 2))
        ttk.Label(search_frame, text="Busnr:").grid(row=0, column=2, sticky="w", pady=(5, 2))

        ttk.Entry(search_frame, textvariable=self._dashboard_controller.address_search_from['street']).grid(
            row=1, column=0, padx=5, pady=5, sticky="ew"
        )
        ttk.Entry(search_frame, width=5, textvariable=self._dashboard_controller.address_search_from['huisnummer']).grid(
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )
        ttk.Entry(search_frame, width=5,
                  textvariable=self._dashboard_controller.address_search_from['busnummer']).grid(
            row=1, column=2, padx=5, pady=5, sticky="ew"
        )

        # Tweede rij met Postcode & Gemeente
        ttk.Label(search_frame, text="Postcode:").grid(row=2, column=0, sticky="w", pady=(10, 2))
        ttk.Label(search_frame, text="Gemeente:").grid(row=2, column=1, sticky="w", pady=(10, 2))

        ttk.Entry(search_frame, textvariable=self._dashboard_controller.address_search_from['postcode'],width=6).grid(
            row=3, column=0, padx=5, pady=5, sticky="ew"
        )
        gemeente_combo = ttk.Combobox(search_frame,values=self._dashboard_controller.gemeenten_namen, state="readonly", textvariable=self._dashboard_controller.address_search_from['gemeente'])
        gemeente_combo.grid(
            row=3, column=1, padx=5, pady=5, sticky="ew", columnspan=2
        )

        gemeente_combo.bind("<<ComboboxSelected>>", self._dashboard_controller.on_gemeente_change)

        search_btn_last_row = 6
        for action in self._dashboard_controller.get_address_search_form_actions():
            ttk.Button(search_frame, text=action['name'], bootstyle=action['style'], command=action['command']).grid(row=search_btn_last_row, column=0, pady=5, padx=20, sticky="ew")
            search_btn_last_row += 1

    def _build_tree_view(self):
        tree_frame = ttk.Frame(self._tab_address)
        tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self._tab_address.grid_rowconfigure(1, weight=1)

        ttk.Label(tree_frame, text="Persoonlijst").grid(row=0, column=0, pady=5, sticky="w")

        columns = ("nummer","Achternaam", "Voornaam", "Geboortedatum", "Geboorteplaats", "Overlijdensdatum", "Overlijdensplaats", "Overlijdensoorzaak", "Wonend sinds", "Verhuist op")
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

