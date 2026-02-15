from tkinter import LEFT, TOP

from ttkbootstrap import BooleanVar, Checkbutton, Frame, Label

from qcm.model.reponse import ReponseQCMultiples
from qcm.vue.parent import Parent

from .ui import CorrectionUI

class CorrectionQCUI(CorrectionUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseQC du model.
    Met en place un layout "Vos réponses" à gauche et "Correction" à droite
    Classe générique implémentée pour les différents types de ReponseQC.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        haut = Frame(self.container)
        haut.pack(side=TOP, fill="x", expand=True)

        vos_reponses = Label(haut, text="Vos réponses :")
        vos_reponses.pack(side=LEFT)

        correction = Label(haut, text="Correction :")
        correction.pack(side="right")
