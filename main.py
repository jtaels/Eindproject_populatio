import sqlite3
import tkinter
from tkinter import messagebox
import controller.AppController as appController
import ui.AppUi as appUi
import os

import db.Database as database

#default password @minD!3St#Pl

DB_NAME = "bevolkingsregister.db"
PROJECT_DIR = "c:\\bevolkingsregister\\"
debug = True

'''

Open het startscherm

'''
def openUi():

    controller = appController.AppController()
    ui = appUi.appUi(controller)

    ui.render()

def showExceptionMessage(message:str,exceptionError):

    if debug:
        message += f"\n Debuginformatie: {exceptionError}"

    messagebox.showwarning("Fout", message)

def main():

    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)

    db = database.Database(DB_NAME)

    try:

        db.connection()

        openUi()

    except sqlite3.Error as error:
        showExceptionMessage("Kan geen verbinding met database maken. Het programma kan niet worden opgestart!",error)

if __name__ == "__main__":

    main()