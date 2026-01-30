from ttkbootstrap import Frame, Entry, StringVar, BooleanVar, Checkbutton, Spinbox, IntVar, Label, Button
from tkinter import TOP, BOTTOM, LEFT, RIGHT

from vue.editeur.editeur_callback_type import CallbackCommand

class Editeur(Frame):
    def __init__(self, parent, page_callback, titre="Énoncé de la question", obligatoire=True, points=1):
        super().__init__(parent, width=600, borderwidth=2, relief="solid")

        self.haut = Frame(self)
        self.haut.pack(side=TOP, fill="x", expand=True)
        self.titre_var = StringVar(value=titre)
        self.titre_entry = Entry(self.haut, textvariable=self.titre_var)
        self.titre_entry.pack(side=LEFT)

        self.points_var = IntVar(value=points)
        self.points_entry = Spinbox(self.haut, textvariable=self.points_var, from_=0, to=1e3, width=4)
        self.points_entry.pack(side=RIGHT)
        points_label = Label(self.haut, text="Points :")
        points_label.pack(side=RIGHT)

        self.milieu = Frame(self)
        self.milieu.pack(fill="x", expand=True)

        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM, fill="x", expand=True)
        self.obligatoire_var = BooleanVar(value=obligatoire)
        obligatoire_ui = Checkbutton(self.bas, text="Obligatoire", variable=self.obligatoire_var)
        obligatoire_ui.pack(side=LEFT)

        delete_button = Button(self.bas, text=" ⤫ ", command=lambda: page_callback(CallbackCommand.DELETE, self), style="warning")
        delete_button.pack(side=RIGHT)

        duplicate_button = Button(self.bas, text=" D ", command=lambda: page_callback(CallbackCommand.DUPLICATE, self), style="info")
        duplicate_button.pack(side=RIGHT)

        each_move_down = Button(self.bas, text=" 🠋 ", command=lambda: page_callback(CallbackCommand.MOVE_DOWN, self))
        each_move_down.pack(side=RIGHT)

        each_move_up = Button(self.bas, text=" 🠉 ", command=lambda: page_callback(CallbackCommand.MOVE_UP, self))
        each_move_up.pack(side=RIGHT)
