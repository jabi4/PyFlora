from PIL import Image
import tkinter as tk
import customtkinter as ctk
from GUI.screens.LoginScreen import LoginScreen
from service.UserService import UserService
from service.PlantService import PlantService
from datasource.tk.TKUser import TkUser


class MainScreen(ctk.CTkFrame):

    def __init__(self, mainWindow, service: UserService, plantService: PlantService):
        super().__init__(master=mainWindow)
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.service = service
        self.plantService = plantService
        self.tkUser = TkUser()
        self.createLoginScreen()
        self.userInfoDisplay()

    def createLoginScreen(self):
        logScreen = LoginScreen(self, self.service, self.tkUser, self.plantService)
        logScreen.grid()


    def userInfoDisplay(self):



        self.userInfo = ctk.CTkFrame(self.master)
        self.userInfo.grid(row=0, column=0, pady=5, padx=5)

        imgUser = Image.open("./GUI/img/user.png")
        self.tkimgUser = ctk.CTkImage(imgUser)
        self.lblimgUser = ctk.CTkLabel(self.userInfo, text="", image=self.tkimgUser)
        self.lblimgUser.grid(row=0, column=0, padx=5, pady=5)

        # self.upozorenje = tk.StringVar()
        # self.lblPozdrav = ctk.CTkLabel(self.userInfo, textvariable=self.pozdrav)
        # self.lblPozdrav.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        self.username = ctk.CTkLabel(self.userInfo, textvariable=self.tkUser.name)
        self.username.grid(row=1, column=0, pady=5, padx=5)

        self.userLastname = ctk.CTkLabel(self.userInfo, textvariable=self.tkUser.surname)
        self.userLastname.grid(row=2, column=0, pady=5, padx=5)

    def updateUserInfo(self):
        self.username.config(text=self.tkUser.name.get())
        self.userLastname.config(text=self.tkUser.surname.get())


# screen = MainScreen()
# screen.tkUser.name.set("Novo ime")
# screen.tkUser.surname.set("Novo prezime")
# screen.updateUserInfo()
