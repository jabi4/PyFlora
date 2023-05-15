import sqlite3
from tkinter import Tk
from customtkinter import CTk
from GUI.screens.LoginScreen import LoginScreen
from service.UserService import UserService
from datasource.tk.TKUser import TkUser
from datasource.dto.UserDto import UserDto

class App(CTk):

    def __init__(self, service: UserService):
        super().__init__()
        self.title("PyFlora")
        self.geometry("1000x600")
        self.service = service
        self.createPrviProzor()

    def createPrviProzor(self):
        LoginScreen(self, self.service)

def initDB():
    DB = "Users.db"
    conn = sqlite3.connect(DB)
    return conn

if __name__ == '__main__':
    connection = initDB()
    service = UserService(connection)
    app = App(service)
    app.mainloop()



