from ttkbootstrap import Frame, Entry, StringVar, BooleanVar, Checkbutton, Spinbox, IntVar, Label, Button, Combobox
from tkinter import TOP, BOTTOM, LEFT, RIGHT

from model.question import Question

class ReponseUI(Frame):
    def __init__(self, parent, question: Question):
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
        pass
