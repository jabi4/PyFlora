from tkinter import StringVar, BooleanVar, IntVar
from datasource.dto.PlantDto import PlantDTO


class TkPlant:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.photo = StringVar()
        self.description = StringVar()
        self.zalijevanje = StringVar()
        self.osvjetljenje = StringVar()
        self.toplina = StringVar()
        self.dohrana = BooleanVar()

    def fillFromDto(self, plantDto):
        self.id = plantDto.id
        self.name.set(plantDto.name)
        self.photo.set(plantDto.photo)
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