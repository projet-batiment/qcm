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
    START = "Commencer..."
    VERIFY = "Corriger"

    def __init__(self, parent: Parent, controller: "Control"):
        """
        Args:
            parent (Parent): the parent container
            controller (Control): the application controller
        """

        super().__init__(parent)
        self.controller = controller

        self.qcm = Menu(self, tearoff=0)
        self.add_cascade(label="QCM", menu=self.qcm)

        self.qcm.add_command(label=self.NEW, command=controller.new_qcm)
        self.qcm.add_command(label=self.OPEN, command=controller.open_qcm)
        self.qcm.add_command(label=self.SAVE, command=controller.save_qcm)
        self.qcm.add_command(label=self.SAVE_AS, command=controller.save_qcm_as)
        self.qcm.add_command(label=self.CLOSE, command=controller.close_qcm)

        self.tentative = Menu(self, tearoff=0)
        self.add_cascade(label="Tentative", menu=self.tentative)

        self.tentative.add_command(label=self.START, command=controller.start_tentative)
        self.tentative.add_command(
            label=self.VERIFY, command=controller.verifier_tentative
        )
        self.tentative.add_command(label=self.SAVE, command=controller.save_tentative)
        self.tentative.add_command(
            label=self.SAVE_AS, command=controller.save_tentative_as
        )
        self.tentative.add_command(label=self.CLOSE, command=controller.close_tentative)

    def has_tentative(self, has_tentative: bool):
        if has_tentative:
            self.tentative.entryconfig(self.SAVE, state="normal")
            self.tentative.entryconfig(self.SAVE_AS, state="normal")
            self.tentative.entryconfig(self.CLOSE, state="normal")
            self.tentative.entryconfig(self.VERIFY, state="normal")
        else:
            self.tentative.entryconfig(self.SAVE, state="disabled")
            self.tentative.entryconfig(self.SAVE_AS, state="disabled")
            self.tentative.entryconfig(self.CLOSE, state="disabled")
            self.tentative.entryconfig(self.VERIFY, state="disabled")

    def has_qcm(self, has_qcm: bool):
        if has_qcm:
            self.qcm.entryconfig(self.SAVE, state="normal")
            self.qcm.entryconfig(self.SAVE_AS, state="normal")
            self.qcm.entryconfig(self.CLOSE, state="normal")
        else:
            self.qcm.entryconfig(self.SAVE, state="disabled")
            self.qcm.entryconfig(self.SAVE_AS, state="disabled")
            self.qcm.entryconfig(self.CLOSE, state="disabled")
