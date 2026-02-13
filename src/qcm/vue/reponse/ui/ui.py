from tkinter import BOTTOM, LEFT, RIGHT, TOP

from ttkbootstrap import Frame, Label

from qcm.model.question import Question
from qcm.vue.parent import Parent


class ReponseUI(Frame):
    """
    Conteneur de l'interface graphique pour éditer une Reponse du model.
    Classe générique implémentée pour les différents types de Reponse.
    """

    def __init__(self, parent, question: Question):
        """
        Args:
            parent (Parent): conteneur parent
            question (Question): la question du model à laquelle répondre
        """

        super().__init__(parent, width=600, borderwidth=2, relief="solid")

        self.question = question

        self.haut = Frame(self)
        self.haut.pack(side=TOP, fill="x", expand=True, pady=5)

        self.titre = Label(self.haut, text=question.enonce)
        self.titre.pack(side=LEFT, padx=5)

        points = Label(self.haut, text=f"Points : {question.points}")
        points.pack(side=RIGHT)

        self.milieu = Frame(self)
        self.milieu.pack(fill="x", expand=True, padx=10, pady=10)
        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM, fill="x", expand=True, pady=5)

        # TODO: mettre à jour le model
        # if reponse.question.requis:
        #     obligatoire = Label(self.bas, "Réponse requise")
        #     obligatoire.pack(side=LEFT, padx=10)

    def corriger(self) -> None:
        # TODO: nécessaire / utile ??
        pass
