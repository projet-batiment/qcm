from tkinter import BOTTOM, LEFT, RIGHT, TOP

from ttkbootstrap import Frame, Label

from qcm.model.reponse import Reponse


class CorrectionUI(Frame):
    """
    Conteneur de l'interface graphique pour afficher une Correction.
    Classe générique implémentée pour les différents types de Reponse.
    """

    def __init__(self, parent, reponse: Reponse):
        """
        Args:
            parent (Parent): conteneur parent
            reponse (Reponse): la réponse du model
        """

        super().__init__(parent, width=600, borderwidth=2, relief="solid")

        self.reponse = reponse

        self.haut = Frame(self)
        self.haut.pack(side=TOP, fill="x", expand=True)

        self.haut_haut = Frame(self.haut)
        self.haut_haut.pack(side=TOP, fill="x", expand=True, pady=5)

        self.haut_bas = Frame(self.haut)
        self.haut_bas.pack(side=TOP, fill="x", expand=True, pady=5)

        self.titre = Label(self.haut_haut, text=reponse.question.enonce)
        self.titre.pack(side=LEFT, padx=5)

        points = Label(self.haut_haut, text=f"Points obtenus : {reponse.points} / {reponse.question.points}")
        points.pack(side=RIGHT)

        result = "correcte" if self.reponse.verifier() else "erronée"
        self.feedback = Label(self.haut_bas, text=f"Réponse {result}.")
        self.feedback.pack(side=LEFT, padx=5)

        self.milieu = Frame(self)
        self.milieu.pack(fill="x", expand=True, padx=10, pady=10)
        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM, fill="x", expand=True, pady=5)
