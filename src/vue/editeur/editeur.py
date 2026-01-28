from ttkbootstrap import Frame, Entry, StringVar, BooleanVar, Checkbutton
from tkinter import TOP, BOTTOM, LEFT, RIGHT

class Editeur(Frame):
    def __init__(self, parent, titre="Énoncé de la question", obligatoire=True):
        super().__init__(parent)

        self.haut = Frame(self)
        self.haut.pack(side=TOP)
        self.titre_var = StringVar(value=titre)
        self.titre_entry = Entry(self.haut, textvariable=self.titre_var)
        self.titre_entry.pack(side=LEFT)

        self.milieu = Frame(self)
        self.milieu.pack()

        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM)
        self.obligatoire_var = BooleanVar(value=obligatoire)
        obligatoire_ui = Checkbutton(self.bas, text="Requis", variable=self.obligatoire_var)
        obligatoire_ui.pack(side=LEFT)
