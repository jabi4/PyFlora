
class PlantDTO:
    def __init__(self):
        self.id = None
        self.name = None
        self.photo = None
        self.description = None
        self.zalijevanje = None
        self.osvjetljenje = None
        self.toplina = None
        self.dohrana = None

    def __repr__(self):
        return str(self.__dict__)

    def getInfo(self):
        return f"{self.name}"

    @staticmethod
    def createFromResult(result: tuple):
        plantDto = PlantDTO()
        plantDto.id = result[0]
        plantDto.name = result[1]
        plantDto.photo = result[2]
        plantDto.description = result[3]
        plantDto.zalijevanje = result[4]
        plantDto.osvjetljenje = result[5]
        plantDto.toplina = result[6]
        plantDto.dohrana = result[7]
        return plantDto

    @staticmethod
    def createFromTkModel(tkModel):
        plantDto = PlantDTO()
        plantDto.id = tkModel.id
        plantDto.name = tkModel.name.get()
        plantDto.photo = tkModel.photo.get()
        plantDto.description = tkModel.description.get()
        plantDto.zalijevanje = tkModel.zalijevanje.get()
        plantDto.osvjetljenje = tkModel.osvjetljenje.get()
        plantDto.toplina = tkModel.toplina.get()
        plantDto.dohrana = tkModel.dohrana.get()
        return plantDto