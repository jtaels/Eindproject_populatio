from fileinput import close
from tkinter import StringVar
from tkinter import messagebox

class AddPersonSubformController:

    def __init__(self, address_result_tree):

        self.address_result_tree = address_result_tree

        self.result_tree = None
        self.on_select = None
        self.add_person_sub_form_ui = None

    def search_person(self, results:list):

        self._fill_tree(results)

    def _fill_tree(self, results):

        self._clear_tree()

        for result in results:
            achternaam = result.achternaam
            voornaam = result.voornaam
            bevolkingsregisternr = result.bevolkingsregisternummer

            self.result_tree.insert(
                "",
                "end",
                values=(bevolkingsregisternr,voornaam,achternaam),
                tags=[result.id]
            )

    def _clear_tree(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def confirm_selection(self):

        selected = self.result_tree.selection()

        if not selected:

            messagebox.showinfo("Info", "Je moet een persoon selecteren!")
            return

        item_id = selected[0]
        tags = self.result_tree.item(item_id, "tags")

        #id doorsturen naar vorig scherm
        self.on_select(tags[0])

        self.add_person_sub_form_ui.destroy()