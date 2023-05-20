from tkinter import StringVar, BooleanVar
# from datasource.dto.UserDto import UserDto # privermeni import koji ce mi pomoc unos podataka

class TkUser:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.surname = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.admin = BooleanVar()

    def fillFromDto(self, userDto):
        self.id = userDto.id
        self.name.set(userDto.name)
        self.surname.set(userDto.surname)
        self.username.set(userDto.username)
        self.password.set(userDto.password)
        self.admin.set(userDto.isAdmin)

    def clear(self):
        self.id = None
        self.name.set("")
        self.surname.set("")
        self.username.set("")
        self.password.set("")
        self.admin.set(False)