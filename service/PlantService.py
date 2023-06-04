from  utils.DBUtils import DBUtils
from datasource.dto.PlantDto import PlantDTO


class PlantService:

    TABLE_NAME = "plants"

    def __init__(self, sqlConnection):
        self.connection = sqlConnection
        self.createTable()
        self._createPlants()

    def createTable(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            VARCHAR(30) NOT NULL UNIQUE,
            foto            VARCHAR(30),
            description     TEXT,
            zalijevanje     VARCHAR(30),
            osvjetljenje    VARCHAR(30),
            toplina         VARCHAR(30),
            dohrana         BOOLEAN NOT NULL);
            
            """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def createPlant(self, name, foto, description, zalijevanje, osvjetljenje, toplina, dohrana):
        query = f"""
                   INSERT INTO {self.TABLE_NAME} (name, foto, description, zalijevanje, osvjetljenje, toplina, dohrana)
                   VALUES ('{name}', '{foto}', '{description}', '{zalijevanje}', '{osvjetljenje}', '{toplina}', {dohrana});
                   """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def _createPlants(self):
        self.createPlant("Bijeli sljez", "plants/bijeli_sljez.jpg", "plants/bijeli_sljez.txt", "Mjesecno", "Sjenovito", "Umjerena",False)
        self.createPlant("Dalmatinski Buhac", "plants/dalmatinski_buhac.jpg", "plants/dalmatinski_buhac.txt", "Tjedno", "Jarko", "Toplija", True)
        self.createPlant("Kadulja", "plants/kadulja.jpg", "plants/kadulja.txt", "Tjedno", "Jarko", "Toplija", True)
        self.createPlant("Lavanda", "plants/lavanda.jpg", "plants/lavanda.txt", "Dnevno", "Sjenovito", "Umjerena", True)
        self.createPlant("Limuska Trava", "plants/limunska_trava.jpg", "plants/limunska_trava.txt", "Dnevno", "Jarko","Toplija", False)
        self.createPlant("Lovor", "plants/lovor.jpg", "plants/lovor.txt", "Tjedno", "Sjenovito", "Toplija", True)
        self.createPlant("Metvica", "plants/metvica.jpg", "plants/metvica.txt", "Dnevno", "Jarko", "Toplija", False)
        self.createPlant("Ruzmarin", "plants/ruzmarin.jpg", "plants/ruzmarin.txt", "Tjedno", "Sjenovito", "Toplija", False)
        self.createPlant("Persin", "plants/persin.jpg", "plants/persin.txt", "Dnevno", "Sjenovito", "Umjerena", True)
        self.createPlant("Ruzmarin", "plants/ruzmarin.jpg", "plants/ruzmarin.txt", "Tjedno", "Jarko", "Toplija", False)
        self.createPlant("Vrijesak", "plants/vrijesak.jpg", "plants/vrijesak.txt", "Dnevno", "Sjenovito", "Umjerena", True)

    # def getAllPlants(self):
    #     plants = []
    #     query = f"SELECT * FROM {self.TABLE_NAME}"
    #     rows = DBUtils.dohvatiPodatke(self.connection, query)
    #     for row in rows:
    #         newPlantDto = PlantDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    #         plants.append(newPlantDto)
    #     return plants

    def getAllPlants(self):
        query = f"SELECT * FROM {self.TABLE_NAME};"
        result = DBUtils.dohvatiPodatke(self.connection, query)
        plants = []
        if result is not None:
            for name in result:
                plantsDto = PlantDTO.createFromResult(name)
                plants.append(plantsDto)
            return plants

    def getPlantById(self, plant_id):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = {plant_id};"

        result = DBUtils.dohvatiPodatke(self.connection, query, True)

        if result is not None:
            newPlantDto: PlantDTO = PlantDTO.createFromResult(result)
            return newPlantDto
        else:
            return None

    def getPlantByName(self, name):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE name = '{name}';"
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            plantDto: PlantDTO = PlantDTO.createFromResult(result)
            return plantDto
        else:
            return None


    def addOrUpdatePlant(self, dto: PlantDTO):
        configuration = self._ifConfigExists(dto.name)
        if configuration is None:
            query = f"""
                    INSERT INTO {self.TABLE_NAME} 
                    (name, foto, description, zalijevanje, osvjetljenje, toplina, dohrana)
                    VALUES 
                    ('{dto.name}', '{dto.photo}', '{dto.description}', '{dto.zalijevanje}', '{dto.osvjetljenje}', '{dto.toplina}', {dto.dohrana});
            """
        else:
            query = f"""
                   UPDATE {self.TABLE_NAME}
                   SET name='{dto.name}',foto='{dto.photo}', description='{dto.description}', zalijevanje='{dto.zalijevanje}', osvjetljenje='{dto.osvjetljenje}', toplina='{dto.toplina}', dohrana={dto.dohrana}
                   WHERE name={dto.name};
            """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def updatePlant(self, dto: PlantDTO):
        query = f"""
                UPDATE {self.TABLE_NAME}
                SET name='{dto.name}',description='{dto.description}', zalijevanje='{dto.zalijevanje}', osvjetljenje='{dto.osvjetljenje}', toplina='{dto.toplina}'
                WHERE id={dto.id};
                """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def deleteplant(self, id):
        query = f"DELETE FROM {self.TABLE_NAME} WHERE id={id};"
        DBUtils.izvrsiIZapisi(self.connection, query)


    def _ifConfigExists(self, name):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE name = '{name}';"
        return DBUtils.dohvatiPodatke(self.connection, query, one=True)
