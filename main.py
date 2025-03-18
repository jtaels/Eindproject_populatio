import sqlite3
import tkinter
from tkinter import messagebox
import controller.AppController as appController
import ui.AppUi as appUi

import db.Database as database

#default password @minD!3St#Pl

DB_NAME = "bevolkingsregister.db"
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

    db = database.Database(DB_NAME)

    try:

        db.connection()

        openUi()

    except sqlite3.Error as error:
        showExceptionMessage("Kan geen verbinding met database maken. Het programma kan niet worden opgestart!",error)

if __name__ == "__main__":

    main()