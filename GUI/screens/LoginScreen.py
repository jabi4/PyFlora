import tkinter
from tkinter import Frame
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
from time import sleep as delay
from PIL import Image, ImageTk
import customtkinter as ctk
from service.UserService import UserService
from datasource.tk.TKUser import TkUser
from datasource.dto.UserDto import UserDto
# root - parent
# frame - parent
# labelframe - parent
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class LoginScreen(ctk.CTkFrame):

    def __init__(self, mainWindow, service: UserService):
        super().__init__(master=mainWindow)
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.service = service
        self.tkUser = TkUser()
        self.userDto = UserDto()
        self['relief'] = tk.RAISED
        self['borderwidth'] = 5
        self.toggleProzor2 = False
        self.toggleVisibility = False
        self.loginScreen()


    def setComponent(self, component, row, column, sticky=None, columnspan=None):
        if not (sticky, columnspan):
            component.grid(row=row, column=column, pady=5, padx=5)
        else:
            component.grid(row=row, column=column, pady=5, padx=5, sticky=sticky, columnspan=columnspan)

    # def createHeader(self):
    #     header = ctk.CTkLabel(self, text="Prijava", font=("Roboto", 24))
    #     self.setComponent(header, 0, 0)


    def loginScreen(self):


        imgShow = Image.open("./GUI/img/show.png")
        imgHide = Image.open("./GUI/img/hide.png")

        self.loginWindow = ctk.CTkFrame(self)
        self.loginWindow.grid(row=0, column=0, pady=5, padx=5)

        header = ctk.CTkLabel(self.loginWindow, text="Prijava:", font=("Roboto", 24))
        self.setComponent(header, 0, 0)

        self.lblUsername = ctk.CTkLabel(self.loginWindow, text="Username:")
        self.lblUsername.grid(row=1, column=0, padx=5, pady=5)

        self.username = tk.StringVar()
        self.eUsername = ctk.CTkEntry(self.loginWindow, textvariable=self.tkUser.username)
        self.eUsername.grid(row=1, column=1, padx=5, pady=5)

        self.lblPassword = ctk.CTkLabel(self.loginWindow, text="Password:")
        self.lblPassword.grid(row=2, column=0, pady=5, padx=5)

        self.tkimgShow = ctk.CTkImage(imgShow)
        self.tkimgHide = ctk.CTkImage(imgHide)

        self.btnToggleVisibility = ctk.CTkButton(self.loginWindow, image=self.tkimgHide, text="", command=self.show_hidePass, height=3, width=3)
        self.btnToggleVisibility.grid(row=2, column=2)

        self.password = tk.StringVar()
        self.ePassword = ctk.CTkEntry(self.loginWindow, show="*", textvariable=self.tkUser.password)
        self.ePassword.grid(row=2, column=1, padx=5, pady=5)

        self.ePassword.bind("<Return>", self.loginEnter)

        btnLogin = ctk.CTkButton(self.loginWindow, text="Login", command=self.login)
        btnLogin.grid(row=3, column=1, pady=5, padx=5)

        rememberMe = ctk.CTkCheckBox(self.loginWindow, text="Remember Me")
        rememberMe.grid(row=3, column=2, pady=5, padx=5)

        self.upozorenje = tk.StringVar()
        self.lblUpozorenje = ctk.CTkLabel(self.loginWindow, textvariable=self.upozorenje)
        self.lblUpozorenje.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

    def show_hidePass(self):
        if not self.toggleVisibility:
            self.ePassword.configure(show="")
            self.btnToggleVisibility.configure(image=self.tkimgShow)
            self.toggleVisibility = True
        else:
            self.ePassword.configure(show="*")
            self.btnToggleVisibility.configure(image=self.tkimgHide)
            self.toggleVisibility = False
    # def togglePassVisibility(self):
    #     if self.ePassword("show") == "":
    #         self.ePassword.config(show="*")
    #         self.btnToggleVisibility.config(image=self.tkimgHide)
    #     else:
    #         self.ePassword.config(show="")
    #         self.btnToggleVisibility.config(image=self.tkimgShow)

    def login(self):
        # self.prozor1.grid_remove()
        # self.creatAdminPanel()
        user = self.service.getUser(self.tkUser.username.get(), self.tkUser.password.get())
        if user is not None:
            self.userDto = user
            self.tkUser.fillFromDto(self.userDto)
            if self.tkUser.admin:
                admin = self.service.getAdminByUsernameAndPass(self.tkUser.username.get(), self.tkUser.password.get(), True)
                if admin is not None:
                    self.upozorenje.set("Success, you are logged in as admin")
                    self.loginWindow.grid_remove()
                    self.adminMenuFrame()

                else:
                    self.upozorenje.set("Success, you are logged in")
        else:
            self.upozorenje.set("Error, Incorrect username or password.")




    # def login(self):
    #     username = self.tkUser.username.set(self.userDto.username)
    #     password = self.tkUser.password.set(self.userDto.password)
    #     isAdmin = self.tkUser.admin
    #
    #
    #     if not username or not password:
    #         self.upozorenje.set("Error, Please enter a username and password.")
    #
    #     else:
    #         if isAdmin:
    #             userDto = self.service.getAdminByUsernameAndPass(self.tkUser.username.get(), self.tkUser.password.get(), self.tkUser.admin.get())
    #         else:
    #             userDto = self.service.getUser(self.tkUser.password.get(), self.tkUser.username.get())
    #
    #             if userDto is None:
    #                 self.upozorenje.set("Success Welcome!")
    #                 self.prozor1.grid_remove

    def loginEnter(self, event):
        self.login()

    def adminMenuFrame(self):

        imgMenu = Image.open("./GUI/img/menu.png")
        imgEdit = Image.open("./GUI/img/edit.png")

        self.tkimgMenu = ctk.CTkImage(imgMenu)
        self.tkimgEdit = ctk.CTkImage(imgEdit)

        self.amFrame = ctk.CTkFrame(self)
        self.amFrame.grid(row=0, column=0, pady=5, padx=5)

        self.btnMenu = ctk.CTkButton(self.amFrame, image=self.tkimgMenu, text="", command=self.mainManu)
        self.btnMenu.grid(row=0, column=0, padx=15, pady=15)

        self.btnAdmin = ctk.CTkButton(self.amFrame, image=self.tkimgEdit, text="", command=self.editUser)
        self.btnAdmin.grid(row=1, column=0, padx=15, pady=15)




    def editUser(self):

        self.userList = []  # Inicijalizacija userList
        self.tkUser = TkUser()

        self.amFrame.grid_remove()
        self.editUserFrame = ctk.CTkFrame(self)
        self.editUserFrame.grid(row=0, column=0, pady=15, padx=15)

        self.lbUsers = tk.Listbox(self.editUserFrame, bg="#333333", font=("Roboto", 12), fg="white", selectbackground="#106A43")
        self.lbUsers.grid(row=0, column=0, pady=10, padx=10, rowspan=6)
        self.lbUsers.bind("<Double-1>", self.selectUserFromList)

        self.fetchAndSetUserList()

        # self.combobox = ctk.CTkComboBox(self.editUserFrame)
        # self.combobox.grid(row=0, column=0, pady=5, padx=5, rowspan=5)
        # self.combobox.bind("<<ComboboxSelected>>", self.selectUserFromList)

        # self.fetchAndSetUserList()

        lblName = ctk.CTkLabel(self.editUserFrame, text="Name:")
        lblName.grid(row=1, column=1, pady=5, padx=5, sticky=E)
        eName = ctk.CTkEntry(self.editUserFrame, textvariable=self.tkUser.name)
        eName.grid(row=1, column=2, pady=5, padx=5, sticky=tk.EW)

        lblsurname = ctk.CTkLabel(self.editUserFrame, text="Surname:")
        lblsurname.grid(row=2, column=1, pady=5, padx=5, sticky=E)
        eSurname = ctk.CTkEntry(self.editUserFrame, textvariable=self.tkUser.surname)
        eSurname.grid(row=2, column=2, pady=5, padx=5, sticky=tk.EW)

        lblUsername = ctk.CTkLabel(self.editUserFrame, text="Username:")
        lblUsername.grid(row=3, column=1, pady=5, padx=5, sticky=E)
        eUsername = ctk.CTkEntry(self.editUserFrame, textvariable=self.tkUser.username)
        eUsername.grid(row=3, column=2, pady=5, padx=5)

        lblPassword = ctk.CTkLabel(self.editUserFrame, text="Password:")
        lblPassword.grid(row=4, column=1, pady=5, padx=5, sticky=E)
        ePass = ctk.CTkEntry(self.editUserFrame, textvariable=self.tkUser.password)
        ePass.grid(row=4, column=2, pady=5, padx=5)

        lblAdmin = ctk.CTkLabel(self.editUserFrame, text="Admin:")
        lblAdmin.grid(row=5, column=1, pady=5, padx=5, sticky=E)
        isAdmin = ctk.CTkCheckBox(self.editUserFrame, text="", variable=self.tkUser.admin)
        isAdmin.grid(row=5, column=2, padx=5, pady=5, sticky=tk.EW, columnspan=3)

        imgSave = Image.open("./GUI/img/save.png")
        imgDel = Image.open("./GUI/img/delete.png")
        imgClose = Image.open("./GUI/img/close.png")
        imgBack = Image.open("./GUI/img/back.png")

        self.tkimgSave = ctk.CTkImage(imgSave)
        self.tkimgDel = ctk.CTkImage(imgDel)
        self.tkimgClose = ctk.CTkImage(imgClose)
        self.tkimgBack = ctk.CTkImage(imgBack)

        btnSave = ctk.CTkButton(self.editUserFrame, text="", image=self.tkimgSave, command=self.btnSaveClicked, height=5, width=5)
        btnSave.grid(row=6, column=0, padx=5, pady=5)

        btnDel = ctk.CTkButton(self.editUserFrame, text="", image=self.tkimgDel, command=self.btnDeleteClicked, height=5, width=5)
        btnDel.grid(row=6, column=1, padx=5, pady=5)

        btnClose = ctk.CTkButton(self.editUserFrame, text="", image=self.tkimgClose, command=self.btnCancelClicked, height=5, width=5)
        btnClose.grid(row=6, column=2, padx=5, pady=5)

        btnBack = ctk.CTkButton(self.editUserFrame, text="", image=self.tkimgBack, command=self.btnBack, height=5, width=5)
        btnBack.grid(row=6, column=3, padx=10, pady=10)

    def mainManu(self):
        pass
    #glavni prozor s biljkama i uredenjem oko njih

    def btnSaveClicked(self):
        userDto = UserDto.createFromTkModel(self.tkUser)
        self.service.updateUser(userDto)
        self.fetchAndSetUserList()

    def btnCancelClicked(self):
        self.tkUser.clear()

    def btnBack(self):
        self.editUserFrame.grid_remove()
        self.adminMenuFrame()

    def btnDeleteClicked(self):
        self.service.deleteUser(self.tkUser.id)
        self.tkUser.clear()
        self.fetchAndSetUserList()




    def fetchAndSetUserList(self):
        self.userList = self.service.getAllUsers()
        simplifiedUserList = []
        if self.userList is not None:
            for user in self.userList:
                u: UserDto = user
                simplifiedUserList.append(u.getInfo())

            self.tkUserList = StringVar(value=simplifiedUserList)
            self.lbUsers.config(listvariable=self.tkUserList)


    def selectUserFromList(self, event):
        selectedIndex = event.widget.curselection()
        userDto: UserDto = self.userList[selectedIndex[0]]
        print(userDto)
        self.tkUser.fillFromDto(userDto)

    def addUser(self):
        pass











