import sqlite3
import tkinter
from tkinter import Tk
from customtkinter import CTk

from GUI.screens.LoginScreen import LoginScreen
from GUI.screens.MainScreen import MainScreen
from service.UserService import UserService
from datasource.tk.TKUser import TkUser
from datasource.dto.UserDto import UserDto
from service.PlantService import PlantService


class App(CTk):

    def __init__(self, service: UserService, plantService: PlantService):
        super().__init__()
        self.title("PyFlora")
        self.geometry("1000x600")
        self.service = service
        self.plantService = plantService
        self._createScreen()

    def _createScreen(self):
        MainScreen(self, self.service, self.plantService)

def initDB():
    DB = "Users.db"
    conn = sqlite3.connect(DB)
    return conn

if __name__ == '__main__':
    connection = initDB()
    service = UserService(connection)
    plantService = PlantService(connection)
    app = App(service, plantService)
    app.mainloop()