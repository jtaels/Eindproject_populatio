import tkinter as tk
from tkinter import ttk, messagebox

class DashboardUi:

    def __init__(self, controller,main_frame):

        self._controller = controller
        self._root = main_frame