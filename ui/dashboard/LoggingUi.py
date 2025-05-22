import os
import tkinter as tk
from tkinter import scrolledtext

class LoggingUi:
    LOG_PATH = "c:\\bevolkingsregister\\logbestand.log"

    def __init__(self, dashboard_controller=None, tab_address=None):
        self._dashboard_controller = dashboard_controller
        self._tab_address = tab_address

    def build(self):

        # Scrollable text widget
        self.text_area = scrolledtext.ScrolledText(self._tab_address, wrap=tk.WORD, font=("Consolas", 10))
        self.text_area.pack(expand=True, fill='both')

        # Laden van het logbestand
        self.load_log()

    def load_log(self):
        if not os.path.exists(self.LOG_PATH):
            self.text_area.insert(tk.END, "❌ Logbestand niet gevonden.")
            return

        try:
            with open(self.LOG_PATH, "r", encoding="utf-8") as file:
                lines = file.readlines()
                self.text_area.insert(tk.END, ''.join(lines[-500:]))  # laatste 500 regels
        except Exception as e:
            self.text_area.insert(tk.END, f"⚠️ Fout bij lezen van het logbestand: {e}")
