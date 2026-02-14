from tkinter import Menu
from typing import TYPE_CHECKING

from qcm.vue.parent import Parent

if TYPE_CHECKING:
    from qcm.control.controller import Control

class MenuBar(Menu):
    """
    Implémentation de la barre de menu (en haut de l'interface)
    """

    NEW = "Nouveau"
    OPEN = "Ouvrir..."
    SAVE = "Enregistrer"
    SAVE_AS = "Enregistrer sous..."
    CLOSE = "Fermer"

    def __init__(self, parent: Parent, controller: "Control"):
        """
        Args:
            parent (Parent): the parent container
            controller (Control): the application controller
        """

        super().__init__(parent)
        self.controller = controller

        self.file_menu = Menu(self, tearoff=0)
        self.add_cascade(label="Fichier QCM", menu=self.file_menu)

        self.file_menu.add_command(label=self.NEW, command=controller.new_file)
        self.file_menu.add_command(label=self.OPEN, command=controller.open_file)
        self.file_menu.add_command(label=self.SAVE, command=controller.save_file)
        self.file_menu.add_command(label=self.SAVE_AS, command=controller.save_file_as)
        self.file_menu.add_command(label=self.CLOSE, command=controller.close_qcm)

    def has_qcm(self, has_qcm: bool):
        if has_qcm:
            self.file_menu.entryconfig(self.SAVE, state="normal")
            self.file_menu.entryconfig(self.SAVE_AS, state="normal")
            self.file_menu.entryconfig(self.CLOSE, state="normal")
        else:
            self.file_menu.entryconfig(self.SAVE, state="disabled")
            self.file_menu.entryconfig(self.SAVE_AS, state="disabled")
            self.file_menu.entryconfig(self.CLOSE, state="disabled")
