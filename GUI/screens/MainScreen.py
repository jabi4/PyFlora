from tkinter import Frame
import tkinter as tk
import customtkinter as ctk

from mqtt.MqttClient import MqttClient
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
        logScreen = LoginScreen(self, self.service, self.plantService)
        logScreen.grid()


    def userInfoDisplay(self):


        self.userInfo = ctk.CTkFrame(self.master)
        self.userInfo.grid(row=0, column=0, pady=5, padx=5)

        # self.upozorenje = tk.StringVar()
        # self.lblPozdrav = ctk.CTkLabel(self.userInfo, textvariable=self.upozorenje)
        # self.lblUpozorenje.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.username = ctk.CTkLabel(self.userInfo, textvariable=self.tkUser.username)
        self.username.grid(row=0, column=0, pady=5, padx=5)

        self.userLastname = ctk.CTkLabel(self.userInfo, textvariable=self.tkUser.surname)
        self.userLastname.grid(row=1, column=0, pady=5, padx=5)