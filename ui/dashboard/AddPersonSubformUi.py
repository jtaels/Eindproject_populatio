import tkinter as tk
from tkinter import ttk

from controller.dashboard.AddPersonSubformController import AddPersonSubformController
from ui.search.PersonSearchFormUi import PersonSearchFormUi


class AddPersonSubformUi(tk.Toplevel):
    def __init__(self, master, address_result_tree, app_controller,on_select = None):
        super().__init__(master)

        self.add_person_subform_controller = AddPersonSubformController(address_result_tree)

        self.add_person_subform_controller.on_select = on_select

        self.add_person_subform_controller.add_person_sub_form_ui = self
        self.title("Persoon toevoegen")
        self.geometry("600x800")  # Iets ruimer

        # Nieuw frame om je formulier in te bouwen
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(2,2))

        # Laat container meeschalen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Bouw formulier in container
        self.person_search_form = PersonSearchFormUi(container, app_controller, self.add_person_subform_controller.search_person)
        self.person_search_form.build().grid(row=0, column=0, sticky="nsew")

        self._build_result_tree(container)
        self._build_action_buttons(container)

        # Zorg dat parent geblokkeerd wordt
        self.transient(master)
        self.grab_set()
        self.focus()
        self.wait_window(self)

    def _build_result_tree(self, parent):
        # Frame voor de tree
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Treeview kolommen
        columns = ("Bevolkingsregisternummer","Achternaam","Voornaam")
        self.add_person_subform_controller.result_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self.add_person_subform_controller.result_tree.heading(col, text=col)
            self.add_person_subform_controller.result_tree.column(col, width=150, anchor="center")

        self.add_person_subform_controller.result_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar toevoegen
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.add_person_subform_controller.result_tree.yview)
        self.add_person_subform_controller.result_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Grid configuratie voor mooie layout
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def _build_action_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(10, 20), sticky="e")

        # Toevoegen-knop
        toevoegen_button = ttk.Button(
            button_frame,
            text="Persoon toevoegen",
            command=self.add_person_subform_controller.confirm_selection
        )
        toevoegen_button.pack(side="right", padx=5)

        # Annuleren-knop
        annuleren_button = ttk.Button(
            button_frame,
            text="Annuleren",
            command=self.destroy  # Sluit het venster
        )
        annuleren_button.pack(side="right", padx=5)