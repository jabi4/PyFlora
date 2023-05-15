import sqlite3


class DBUtils:

    @staticmethod
    def izvrsiIZapisi(sqlConnection, upit):
        try:
            cursor = sqlConnection.cursor()
            cursor.execute(upit)
            sqlConnection.commit()
            cursor.close()
            print("Akcija uspjesno izvrsena")
            return True
        except sqlite3.Error as sqlError:
            print(sqlError)
        except Exception as e:
            print(e)

        return False

    # @staticmethod
    # def dohvatiListuPodataka(sqlConnection, upit):
    #     try:
    #         cursor: sqlite3.Cursor = sqlConnection.cursor()
    #         cursor.execute(upit)
    #         rezultat = cursor.fetchall()
    #         cursor.close()
    #         print("Akcija dohvati uspjesno izvrsena")
    #         return rezultat
    #     except sqlite3.Error as sqlError:
    #         print(sqlError)
    #     except Exception as e:
    #         print(e)
    #
    # @staticmethod
    # def dohvatiPodatak(sqlConnection, upit):
    #     try:
    #         cursor: sqlite3.Cursor = sqlConnection.cursor()
    #         cursor.execute(upit)
    #         rezultat = cursor.fetchone()
    #         cursor.close()
    #         print("Akcija dohvati uspjesno izvrsena")
    #         return rezultat
    #     except sqlite3.Error as sqlError:
    #         print(sqlError)
    #     except Exception as e:
    #         print(e)

    @staticmethod
    def dohvatiPodatke(sqlConnection, upit, one=False):
        try:
            cursor: sqlite3.Cursor = sqlConnection.cursor()
            cursor.execute(upit)
            rezultat = None
            if one:
                rezultat = cursor.fetchone()
            else:
                rezultat = cursor.fetchall()
            cursor.close()
            print("Akcija dohvati uspjesno izvrsena")
            return rezultat
        except sqlite3.Error as sqlError:
            print(sqlError)
        except Exception as e:
            print(e)


