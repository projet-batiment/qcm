from tkinter import Menu

class MenuBar(Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        file_menu = Menu(self, tearoff=0)
        self.add_cascade(label="Fichier", menu=file_menu)

        file_menu.add_command(label="Créer un nouveau QCM", command=controller.new_file)
        file_menu.add_command(label="Ouvrir un QCM", command=controller.open_file)
        file_menu.add_command(label="Sauvegarder le QCM", command=controller.save_file)
