import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap import ttk
import controller.StartController as StartController
from ttkbootstrap.constants import *

class appUi:

    def __init__(self, controller):

        self._controller = controller
        self._root = tk.Tk()

        self._setup()

    def _setup(self):

        self._root.geometry("600x600")
        self._root.title("Bevolkingsregister")

        # Frame dat de content zal bevatten
        self.contentFrame = ttk.Frame(self._root)
        self.contentFrame.pack(fill=tk.BOTH, expand=True)

        self._controller.switch_screen("start", self.contentFrame)

    def render(self):
        self._root.mainloop()