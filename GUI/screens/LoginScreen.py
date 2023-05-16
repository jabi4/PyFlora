from tkinter import Frame
import tkinter as tk
from tkinter import *
from tkinter import ttk
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
        self.kreirajPrvuGrupuWidgeta()


    def setComponent(self, component, row, column, sticky=None, columnspan=None):
        if not (sticky, columnspan):
            component.grid(row=row, column=column, pady=5, padx=5)
        else:
            component.grid(row=row, column=column, pady=5, padx=5, sticky=sticky, columnspan=columnspan)

    # def createHeader(self):
    #     header = ctk.CTkLabel(self, text="Prijava", font=("Roboto", 24))
    #     self.setComponent(header, 0, 0)


    def kreirajPrvuGrupuWidgeta(self):


        imgShow = Image.open("./GUI/img/show.png")
        imgHide = Image.open("./GUI/img/hide.png")

        self.prozor1 = ctk.CTkFrame(self)
        self.prozor1.grid(row=2, column=0, pady=5, padx=5)

        header = ctk.CTkLabel(self.prozor1, text="Prijava", font=("Roboto", 24))
        self.setComponent(header, 0, 0)

        self.lblUsername = ctk.CTkLabel(self.prozor1, text="Username:")
        self.lblUsername.grid(row=1, column=0, padx=5, pady=5)

        self.username = tk.StringVar()
        self.eUsername = ctk.CTkEntry(self.prozor1, textvariable=self.tkUser.username)
        self.eUsername.grid(row=1, column=1, padx=5, pady=5)

        self.lblPassword = ctk.CTkLabel(self.prozor1, text="Password:")
        self.lblPassword.grid(row=2, column=0, pady=5, padx=5)

        self.tkimgShow = ImageTk.PhotoImage(imgShow)
        self.tkimgHide = ImageTk.PhotoImage(imgHide)

        ttk.Style().configure("TButton", padding=5, relief="flat", background="black")
        self.btnToggleVisibility = ttk.Button(self.prozor1, image=self.tkimgHide, command=self.show_hidePass, style="BW.TLabel")
        self.btnToggleVisibility.grid(row=2, column=2)


        self.password = tk.StringVar()
        self.ePassword = ctk.CTkEntry(self.prozor1, show="*", textvariable=self.tkUser.password)
        self.ePassword.grid(row=2, column=1, padx=5, pady=5)

        self.ePassword.bind("<Return>", self.loginEnter)

        btnLogin = ctk.CTkButton(self.prozor1, text="Login", command=self.login)
        btnLogin.grid(row=3, column=1, pady=5, padx=5)

        rememberMe = ctk.CTkCheckBox(self.prozor1, text="Remember Me")
        rememberMe.grid(row=3, column=2, pady=5, padx=5)

        self.upozorenje = tk.StringVar()
        self.lblUpozorenje = ctk.CTkLabel(self.prozor1, textvariable=self.upozorenje)
        self.lblUpozorenje.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

    def show_hidePass(self):
        if not self.toggleVisibility:
            self.ePassword.configure(show="")
            self.btnToggleVisibility.config(image=self.tkimgShow)
            self.toggleVisibility = True
        else:
            self.ePassword.configure(show="*")
            self.btnToggleVisibility.config(image=self.tkimgHide)
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
            admin = self.service.getAdminByUsernameAndPass(self.tkUser.username.get(), self.tkUser.password.get(), self.tkUser.admin.get())
            self.upozorenje.set("Usa si")
            if admin:
                # self.creatAdminPanel()
                self.upozorenje.set("Usa  admin")

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

    def creatAdminPanel(self):

        self.adminProzor = ctk.CTkFrame(self)
        self.setComponent(self.adminProzor, 0, 0)

        self.adminPanel = ctk.CTkLabel(self.adminProzor, text="Admin panel")
        self.setComponent(self.adminPanel, 0, 0)


        # self.lbUsers = ctk.CTkComboBox(self.adminPanel)
        # self.lbUsers.grid(row=0, column=0, pady=5, padx=5, rowspan=5)
        # self.lbUsers.bind("<Double-1>", self.selectUserFromList())

        self.fetchAndSetUserList()

        lblName = ctk.CTkLabel(self.adminPanel, text="Name:")
        self.setComponent(self.adminPanel, 0, 1)

        name = ctk.CTkEntry(self.adminPanel, textvariable=self.tkUser.name)
        name.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW, columnspan=4)

        surname = ttk.Entry(self.adminPanel, textvariable=self.tkUser.surname)
        surname.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW, columnspan=3)

        UsernameLbl = ctk.CTkLabel(self.prozor1, text="Username:")
        UsernameLbl.grid(row=1, column=0, padx=5, pady=5)

        username = ctk.CTkEntry(self.a)

        password = ttk.Entry(adminPanel, textvariable=self.tkUser.password)
        password.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW, columnspan=3)

        isActive = ttk.Checkbutton(adminPanel, text="Active", variable=self.tkUser.admin)
        isActive.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW, columnspan=3)

        btnSave = ttk.Button(adminPanel, text="Spremi", command=self.btnSaveClicked)
        self.setComponent(btnSave, 4, 1)

        btnCancel = ttk.Button(adminPanel, text="Odustani", command=self.btnCancelClicked)
        self.setComponent(btnCancel, 4, 2)

        btnDelete = ttk.Button(adminPanel, text="Obrisi", command=self.btnDeleteClicked)
        self.setComponent(btnDelete, 4, 3)

    def btnSaveClicked(self):
        userDto = UserDto.createFromTkModel(self.tkUser)
        self.service.updateUser(userDto)
        self.fetchAndSetUserList()

    def btnCancelClicked(self):
        self.clearTkUser()

    def btnDeleteClicked(self):
        self.service.deleteUser(self.tkUser.id)
        self.clearTkUser()
        self.fetchAndSetUserList()

    def clearTkUser(self):
        self.tkUser.clear()

    def selectUserFromList(self, event):
        selectedIndex = event.widget.curselection()
        userDto: UserDto = self.userList[selectedIndex[0]]
        print(userDto)
        self.tkUser.fillFromDto(userDto)

    def fetchAndSetUserList(self):
        self.userList = self.service.getAllUsers()
        simplifiedUserList = []
        for user in self.userList:
            u: UserDto = user
            simplifiedUserList.append(u.getInfo())

        self.tkUserList = StringVar(value=simplifiedUserList)
        self.lbUsers.config(listvariable=self.tkUserList)


    def creatA2Panel(self):
        adminPanel = ttk.LabelFrame(self, text="a2 panel")
        self.setComponent(adminPanel, 3, 0)




