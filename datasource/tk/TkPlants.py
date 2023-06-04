from tkinter import StringVar, BooleanVar, IntVar
from datasource.dto.PlantDto import PlantDTO
from PIL import Image

class TkPlant:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.photo = None
        self.description = StringVar()
        self.zalijevanje = StringVar()
        self.osvjetljenje = StringVar()
        self.toplina = StringVar()
        self.dohrana = BooleanVar()

    def fillFromDto(self, plantDto):
        self.id = plantDto.id
        self.name.set(plantDto.name)
        if plantDto.photo is not None:
            self.photo = Image.open(plantDto.photo)
        else:
            self.photo = None
        # self.photo = plantDto.photo
        self.description.set(plantDto.description)
        self.zalijevanje.set(plantDto.zalijevanje)
        self.osvjetljenje.set(plantDto.osvjetljenje)
        self.toplina.set(plantDto.toplina)
        self.dohrana.set(plantDto.dohrana)

    def clear(self):
        self.id = None
        self.name.set("")
        self.photo = None
        self.description.set("")
        self.zalijevanje.set("")
        self.osvjetljenje.set("")
        self.toplina.set("")
        self.dohrana.set(False)