import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from tkinter.ttk import Style
import customtkinter as ctk
from PIL import Image, ImageTk
from service.PlantService import PlantService
from datasource.dto.PlantDto import PlantDTO
from datasource.tk.TkPlants import TkPlant
from datasource.tk.TkValues import TkValues
import random
import tkinter.filedialog as filedialog




class PlantsScreen(ctk.CTkFrame):

    def __init__(self, parent, plantService: PlantService):
        super().__init__(master=parent)
        self.grid()
        self.tkModelPlant = TkPlant()
        self.plantService = plantService
        self.makeTabs()
        self.simNumbers = TkValues()
        self.populatePlantsTab()
        self.populatePotsTab()

    def makeTabs(self):

        style = Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#333333")
        style.map("TNotebook", background=[("selected", "#106A43")])

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, pady=5, padx=5)

        self.tabPlants = ctk.CTkFrame(self.tabs)
        self.tabPots = ctk.CTkFrame(self.tabs)

        imgPlant = Image.open("./GUI/img/plant.png")
        self.tkimgPlant = ImageTk.PhotoImage(imgPlant)
        imgPot = Image.open("./GUI/img/potted-plant.png")
        self.tkimgPot = ImageTk.PhotoImage(imgPot)


        self.tabs.add(self.tabPlants, text="PLANTS", image=self.tkimgPlant, compound="left")
        self.tabs.add(self.tabPots, text="POTS", image=self.tkimgPot, compound="left")

    def populatePlantsTab(self):

        plants = self.plantService.getAllPlants()
        row_num = 0
        col_num = 0

        for i, plant in enumerate(plants):
            # Create a label for the plant name
            plant_name_label = ctk.CTkLabel(self.tabPlants, text=plant.name)
            plant_name_label.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="w")

            # Load the plant image using PIL and create a Tkinter PhotoImage object
            plant_image = Image.open(plant.photo)
            plant_image = plant_image.resize((100, 100))
            plant_photo = ImageTk.PhotoImage(plant_image)

            # Create a label to display the plant image
            plant_image_label = ttk.Label(self.tabPlants, image=plant_photo, text="")
            plant_image_label.image = plant_photo
            plant_image_label.grid(row=row_num, column=col_num + 1, padx=10, pady=10)
            plant_image_label.bind("<Button-1>", lambda event, index=plant.id: self.showPlantDetails(index))

            # Increment the column number
            col_num += 2

            # If we've reached the end of a row, reset the column number and increment the row number
            if col_num == 8:
                col_num = 0
                row_num += 1

        imgEdit = Image.open("./GUI/img/edit-button.png")
        self.imgEdit = ctk.CTkImage(imgEdit)
        self.editButton = ctk.CTkButton(self.tabPlants, text="", image=self.imgEdit, command=self.editPlants)
        self.editButton.grid(row=3, column=7, padx=5, pady=5)

    """Plant details tab"""

    def showPlantDetails(self, plant_id):
        print(f"Plant ID: {plant_id}")
        plant = self.plantService.getPlantById(plant_id)


        if plant is None:
            messagebox.showerror('Error', 'Plant not found')
            return
        # rjesi da se pomice teks i prelama

        # Create a new Toplevel window to display the plant details
        plant_window = ctk.CTkToplevel(self.master)
        plant_window.title(plant.name)

        # Create a label to display the plant name
        plant_name_label = ctk.CTkLabel(plant_window, text=plant.name)
        plant_name_label.pack(pady=10)

        # Load the plant image using PIL and create a Tkinter PhotoImage object
        plant_image = Image.open(plant.photo)
        plant_image = plant_image.resize((200, 200))
        plant_photo = ImageTk.PhotoImage(plant_image)

        # Create a label to display the plant image
        plant_image_label = ttk.Label(plant_window, image=plant_photo, text="")
        plant_image_label.image = plant_photo
        plant_image_label.pack(pady=10)

        # Create a label to display the plant description
        plant_desc_label = ctk.CTkLabel(plant_window, text=plant.description)
        plant_desc_label.pack(pady=10)

        # Create a button to close the window
        close_button = ctk.CTkButton(plant_window, text="Close", command=plant_window.destroy)
        close_button.pack(pady=10)

    """Pots details tab"""

    def populatePotsTab(self):

        lblInstructions = ctk.CTkLabel(self.tabPots, text="Dvoklikom na ime biljke posadite biljku u posudu, te klikom na gumb Get info dobijate vrijednosti sa senzora.")
        lblInstructions.pack()

        self.plantsList = tk.Listbox(self.tabPots, width=20, height=12, selectmode=tk.SINGLE, bg="#333333", font=("Roboto", 12), fg="white", selectbackground="#106A43")
        self.plantsList.pack(anchor=tk.NW,  expand=True, side=tk.LEFT)
        self.plantsList.bind('<Double-Button-1>', self.plantingThePlantInPot)

        self.plantsInList = self.plantService.getAllPlants()
        for plant in self.plantsInList:
            self.plantsList.insert("end", plant.name)

        self.btnSimulated = ctk.CTkButton(self.tabPots, text="Get info", command=self.simulateNumbers)
        self.btnSimulated.pack(anchor=tk.SW, side=tk.LEFT)

        self.btnMovePlant = ctk.CTkButton(self.tabPots, text="Remove plant from pot", command=self.btnBackClick)
        self.btnMovePlant.pack(anchor=tk.S, side=tk.LEFT)

    def plantingThePlantInPot(self, event):
        plantedPlantName = self.plantsList.get(self.plantsList.curselection())
        self.editPlantDTO = self.plantService.getPlantByName(plantedPlantName)
        print(self.editPlantDTO)

        imgTemp = Image.open("./GUI/img/celsius.png")
        self.imgTemp = ctk.CTkImage(imgTemp)
        imgSun = Image.open("./GUI/img/sun.png")
        self.imgSun = ctk.CTkImage(imgSun)
        imgHum = Image.open("./GUI/img/humidity.png")
        self.imgHum = ctk.CTkImage(imgHum)
        imgPH = Image.open("./GUI/img/ph.png")
        self.imgPH = ctk.CTkImage(imgPH)


        self.potFrame = ctk.CTkFrame(self.tabPots)
        self.potFrame.pack(side=tk.LEFT, expand=True, anchor=tk.S)

        # Load the plant image using PIL and create a Tkinter PhotoImage object
        plant_image = Image.open(self.editPlantDTO.photo)
        plant_image = plant_image.resize((200, 200))
        plant_photo = ImageTk.PhotoImage(plant_image)

        # Create a label to display the plant image
        self.imgPlanted = ttk.Label(self.potFrame, image=plant_photo)
        self.imgPlanted.image = plant_photo
        self.imgPlanted.pack(anchor=tk.NE, expand=True)

        # labels for simulated info
        self.lblSoilMoisture = ctk.CTkLabel(self.potFrame, image=self.imgHum, text="")
        self.lblSoilMoisture.pack()
        self.lvlSoilMoistureValue = ctk.CTkLabel(self.potFrame, textvariable=self.simNumbers.soilMoisture)
        self.lvlSoilMoistureValue.pack()

        self.lblSoilPh = ctk.CTkLabel(self.potFrame, image=self.imgPH, text="")
        self.lblSoilPh.pack()
        self.lblSoilPhValue = ctk.CTkLabel(self.potFrame, textvariable=self.simNumbers.soilPh)
        self.lblSoilPhValue.pack()

        self.lblLight = ctk.CTkLabel(self.potFrame, image=self.imgSun, text="")
        self.lblLight.pack()
        self.lblLightValue = ctk.CTkLabel(self.potFrame, textvariable=self.simNumbers.light)
        self.lblLightValue.pack()

        self.lblAirTemp = ctk.CTkLabel(self.potFrame, image=self.imgTemp, text="")
        self.lblAirTemp.pack()
        self.lblAirTempValue = ctk.CTkLabel(self.potFrame, textvariable=self.simNumbers.airTemp)
        self.lblAirTempValue.pack()


    def editPlants(self):

        self.plantsList = []  # Inicijalizacija userList
        self.tkPlant = TkPlant()


        self.frameEditing = ctk.CTkToplevel(self.master, bd=10)
        self.frameEditing.title(f"Plants edit window")

        self.plantsListName = tk.Listbox(self.frameEditing, width=20, height=12, selectmode=tk.SINGLE, bg="#333333", font=("Roboto", 12), fg="white", selectbackground="#106A43")
        self.plantsListName.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        self.plantsListName.bind("<Double-1>", self.selectPlantFromList)
        self.fetchAndSetPlantsList()



        lblPlantName = ctk.CTkLabel(self.frameEditing, text="Ime biljke:")
        lblPlantName.grid(row=1, column=0, pady=5, padx=5)

        entryPlantName = ctk.CTkEntry(self.frameEditing, textvariable=self.tkModelPlant.name)
        entryPlantName.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        lblPlantZalijevanje = ctk.CTkLabel(self.frameEditing, text="Zalijevanje:")
        lblPlantZalijevanje.grid(row=2, column=0, pady=5, padx=5)

        entryZalijevanje = ctk.CTkEntry(self.frameEditing, textvariable=self.tkModelPlant.zalijevanje)
        entryZalijevanje.grid(row=2, column=1,pady=5, padx=5, sticky=tk.W)

        lblPlantOsvjetljenje = ctk.CTkLabel(self.frameEditing, text="Osvjetljenje:")
        lblPlantOsvjetljenje.grid(row=3, column=0,pady=5, padx=5)

        entryOsvjetljenje = ctk.CTkEntry(self.frameEditing, textvariable=self.tkModelPlant.osvjetljenje)
        entryOsvjetljenje.grid(row=3, column=1,pady=5, padx=5, sticky=tk.W)

        lblPlantToplina = ctk.CTkLabel(self.frameEditing, text="Toplina:")
        lblPlantToplina.grid(row=4, column=0,pady=5, padx=5)

        entryToplina = ctk.CTkEntry(self.frameEditing, textvariable=self.tkModelPlant.toplina)
        entryToplina.grid(row=4, column=1,pady=5, padx=5,sticky=tk.W)

        imgSave = Image.open("./GUI/img/save.png")
        imgDel = Image.open("./GUI/img/delete.png")
        imgClose = Image.open("./GUI/img/close.png")
        imgBack = Image.open("./GUI/img/back.png")
        imgAddimg = Image.open("./GUI/img/add-image.png")

        self.tkimgSave = ctk.CTkImage(imgSave)
        self.tkimgDel = ctk.CTkImage(imgDel)
        self.tkimgClose = ctk.CTkImage(imgClose)
        self.tkimgBack = ctk.CTkImage(imgBack)
        self.tkimgAdd = ctk.CTkImage(imgAddimg)

        self.btnSpremi = ctk.CTkButton(self.frameEditing, text="", image=self.tkimgSave, command=self.btnSave)
        self.btnSpremi.grid(row=1, column=2,pady=5, padx=5,sticky=tk.W)

        self.btnDelete = ctk.CTkButton(self.frameEditing, text="", image=self.tkimgDel, command=self.btnDeletePlant)
        self.btnDelete.grid(row=2, column=2, pady=5, padx=5, sticky=tk.W)

        self.btnCancle = ctk.CTkButton(self.frameEditing, text="", image=self.tkimgClose, command=self.btnCancleClick)
        self.btnCancle.grid(row=3, column=2, pady=5, padx=5, sticky=tk.W)

        self.btnAddImage = ctk.CTkButton(self.frameEditing, text="",image=self.tkimgAdd, command=self.addImage)
        self.btnAddImage.grid(row=4, column=2, pady=5, padx=5, sticky=tk.W)

    # ova metoda nije zavrsena
    def addImage(self):
        # Korisnik odabire sliku iz dijaloškog okvira
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if image_path:
            # Učitajte sliku pomoću PIL-a i stvorite objekt ImageTk.PhotoImage
            plant_image = Image.open(image_path)
            plant_image = plant_image.resize((200, 200))
            plant_photo = ImageTk.PhotoImage(plant_image)

            # Ažurirajte sliku na etiketi
            self.imgPlant.configure(image=plant_photo)
            self.imgPlant.image = plant_photo

            # Spremite putanju do slike u svojstvo tkModelPlant.photo
            self.tkModelPlant.photo = image_path


    def btnSave(self):
        plantDto = PlantDTO.createFromTkModel(self.tkModelPlant)
        self.plantService.updatePlant(plantDto)
        self.fetchAndSetPlantsList()

    def btnDeletePlant(self):
        self.plantService.deleteplant(self.tkModelPlant.id)
        self.tkModelPlant.clear()
        self.fetchAndSetPlantsList()

    def btnCancleClick(self):
        # self.entryPlantName.delete(0, 'end')
        # self.entryPlantDescription.delete(0, 'end')
        # self.photoPath = None
        # self.imagePreview.config(image=None)
        self.tkModelPlant.clear()

    def btnBackClick(self):
        if self.potFrame is not None:
            self.potFrame.destroy()
            self.potFrame = None


    def fetchAndSetPlantsList(self):
        self.plantList = self.plantService.getAllPlants()
        simplifiedPlantList = []
        if self.plantList is not None:
            for plant in self.plantList:
                p: PlantDTO = plant
                simplifiedPlantList.append(p.getInfo())

            self.tkPlantList = StringVar(value=simplifiedPlantList)
            self.plantsListName.config(listvariable=self.tkPlantList)

    def selectPlantFromList(self, event):
        selectedPlantIndex = self.plantsListName.curselection()
        if selectedPlantIndex:
            selectedIndex = selectedPlantIndex[0]
            selectedPlantName = self.plantsListName.get(selectedIndex)
            self.editedPlantDTO = self.plantService.getPlantByName(selectedPlantName)
            if self.editedPlantDTO is not None:
                self.tkModelPlant.fillFromDto(self.editedPlantDTO)
                self.selectedPhotoPath = self.editedPlantDTO.photo
                self.selectedPlantDescription = self.editedPlantDTO.description

                # Prikazivanje slike
                self.showPlantImage(self.selectedPhotoPath)

                # Prikazivanje opisa

                self.showPlantDescription(self.selectedPlantDescription)

    def showPlantImage(self, photo):

        imgPlant = Image.open(photo)
        imgPlant = imgPlant.resize((200, 200))
        photoImg = ImageTk.PhotoImage(imgPlant)

        self.plantImageLabel = tk.Label(self.frameEditing, image=photoImg)
        self.plantImageLabel.image = photoImg
        self.plantImageLabel.grid(row=0, column=2, pady=5, padx=5)

    def showPlantDescription(self, description):
        self.textPlantDescription = tk.Text(self.frameEditing, width=40, height=20, bg="#333333", font=("Roboto", 12),
                                            fg="white", selectbackground="#106A43")
        self.textPlantDescription.grid(row=0, column=1)
        self.textPlantDescription.config(state=tk.NORMAL)
        self.textPlantDescription.insert("1.0", description)

    def simulateNumbers(self):
        mylist = ["Sjenovito", "Jarko"]
        self.simNumbers.soilPh.set(random.randrange(5, 8))
        self.simNumbers.soilMoisture.set(random.randrange(20, 100))
        self.simNumbers.airTemp.set(random.randrange(10, 30))
        self.simNumbers.light.set(random.choice(mylist))
