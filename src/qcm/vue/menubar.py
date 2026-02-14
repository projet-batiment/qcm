from tkinter import Menu
from typing import TYPE_CHECKING

from qcm.vue.parent import Parent

if TYPE_CHECKING:
    from qcm.control.controller import Control


class MenuBar(Menu):
    """
    Implémentation de la barre de menu (en haut de l'interface)
    """

    def __init__(self, parent: Parent, controller: "Control"):
        """
        Args:
            parent (Parent): the parent container
            controller (Control): the application controller
        """

        super().__init__(parent)
        self.controller = controller

        file_menu = Menu(self, tearoff=0)
        self.add_cascade(label="Fichier QCM", menu=file_menu)

        file_menu.add_command(label="Nouveau", command=controller.new_file)
        file_menu.add_command(label="Ouvrir...", command=controller.open_file)
        file_menu.add_command(label="Enregistrer", command=controller.save_file)
        file_menu.add_command(
            label="Enregistrer sous...", command=controller.save_file_as
        )
