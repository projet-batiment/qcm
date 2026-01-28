from ttkbootstrap import Frame, Entry, Radiobutton, IntVar
from tkinter import LEFT, TOP, StringVar

from .editeur import Editeur

class ChoixUnique(Editeur):
    def __init__(self, parent, choix=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix = ["a", "b", "c"] if choix is None else choix
        self.choix_ui = []
        self.choix_var = IntVar(value=-1)
        self.vars = []

        self.update()

    def update(self):
        for each_old_ui in self.choix_ui:
            each_old_ui.pack_forget()

        self.choix_ui = []
        self.vars = []

        for i, each_choix in enumerate(self.choix):
            each_frame = Frame(self.milieu)
            each_frame.pack(side=TOP)

            each_var = StringVar(value=each_choix)
            self.vars.append(each_var)

            each_radio = Radiobutton(each_frame, value=i)
            each_radio.pack(side=LEFT)

            each_entry = Entry(each_frame, textvariable=each_var)
            each_entry.pack(side=LEFT)

            self.choix_ui.append(each_frame)
