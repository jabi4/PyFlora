from utils.DBUtils import DBUtils
from datasource.dto.UserDto import UserDto


class UserService:

    TABLE_NAME = "users"

    def __init__(self, sglConection):
        self.connection = sglConection
        self.createTable()
        self._createUsers()

    def createTable(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                surname VARCHAR(30) NOT NULL,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(10) NOT NULL,
                admin BOOLEAN NOT NULL     
            );
        """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def addUser(self, name, surname, username, password, admin):
        query = f"""
            INSERT INTO {self.TABLE_NAME} (name, surname, username, password, admin )
            VALUES ('{name}', '{surname}', '{username}', '{password}', {admin})
        """
        DBUtils.izvrsiIZapisi(self.connection, query)

#     pomocna funkcija za ubacivanje par korisnika
    def _createUsers(self):
        self.addUser("jasmin", "bilic", "jbilic01", "0000", True)
        self.addUser("Pero", "Peric", "pperic01", "1111", False)
        self.addUser("Ivo", "ivic", "iivic01", "2222", False)
        self.addUser("Ana", "Anic", "aanic01", "3333", False)
        self.addUser("Frane", "Maric", "fmaric01", "4444", False)

    def getUser(self, username, password):
        query = f"SELECT * FROM {self.TABLE_NAME} where username='{username}' AND password='{password}'; "
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            userDto: UserDto = UserDto.creataFromResult(result)
            print(userDto)
            return userDto
        else:
            return None

    def getAdminByUsernameAndPass(self, username, password, isAdmin):
        query = f"SELECT * FROM {self.TABLE_NAME} where username='{username}' and password='{password}' and admin={isAdmin}; "
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            userDto: UserDto = UserDto.creataFromResult(result)
            print(userDto)
            return userDto
        else:
            return None

    def getAllUsers(self):
        query = f"SELECT * FROM {self.TABLE_NAME};"
        result = DBUtils.dohvatiPodatke(self.connection, query)
        userList = []
        if result is not None:
            for user in result:
                userDto = UserDto.creataFromResult(user)
                if userDto.isAdmin == True:
                    continue
        #             ne zelim da mi provjerava admina i da ga imam u listi
                else:
                    userList.append(userDto)
        else:
            return None

    def updateUser(self, dto: UserDto):
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET name='{dto.name}', surname='{dto.surname}', username='{dto.username}', password='{dto.password}', admin={dto.isAdmin}
            WHERE id={dto.id};
        """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def deleteUser(self, id):
        query = f"DELETE FROM {self.TABLE_NAME} where id={id};"
        DBUtils.izvrsiIZapisi(self.connection, query)



