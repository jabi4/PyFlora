# privermeni import koji ce mi pomoc unos podataka
# from datasource.tk.TKUser import TkUser

class UserDto:

    def __init__(self):
        self.id = None
        self.name = None
        self.surname = None
        self.username = None
        self.password = None
        self.isAdmin = None

# repr funkcija ispisuje usera
    def __repr__(self):
        return str(self.__dict__)

    def getInfo(self):
        return f"{self.name} {self.surname}"

    @staticmethod
    def createFromResult(result: tuple):
        userDto = UserDto()
        userDto.id = result[0]
        userDto.name = result[1]
        userDto.surname = result[2]
        userDto.username = result[3]
        userDto.password = result[4]
        userDto.isAdmin = result[5]
        return userDto

    @staticmethod
    def createFromTkModel(tkModel):
        userDto = UserDto()
        userDto.id = tkModel.id
        userDto.name = tkModel.name.get()
        userDto.surname = tkModel.surname.get()
        userDto.username = tkModel.username.get()
        userDto.password = tkModel.password.get()
        userDto.isAdmin = tkModel.admin.get()
        return userDto

