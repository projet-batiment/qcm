from ttkbootstrap import (
    Frame,
    Entry,
    StringVar,
    BooleanVar,
    Checkbutton,
    Spinbox,
    IntVar,
    Label,
    Button,
    Combobox,
)
from tkinter import TOP, BOTTOM, LEFT, RIGHT

from vue.editeur.editeur_callback_type import CallbackCommand


class Editeur(Frame):
    def __init__(
        self,
        parent,
        page_callback,
        titre="Énoncé de la question",
        obligatoire=True,
        points=1,
    ):
        super().__init__(parent, width=600, borderwidth=2, relief="solid")

        self.haut = Frame(self)
        self.haut.pack(side=TOP, fill="x", expand=True, pady=5)
        self.titre_var = StringVar(value=titre)
        self.type_var = StringVar(value="Choix Unique")
        self.points_var = IntVar(value=points)
        self.titre_entry = Entry(self.haut, textvariable=self.titre_var, width=40)
        self.titre_entry.pack(side=LEFT, padx=5)

        self.type_selector = Combobox(
            self.haut,
            textvariable=self.type_var,
            values=["Choix Unique", "Choix Multiple"],
            state="readonly",
            width=15,
        )
        self.type_selector.pack(side=LEFT, padx=10)
        self.type_selector.bind(
            "<<ComboboxSelected>>",
            lambda e: page_callback(CallbackCommand.CHANGE_TYPE, self),
        )

        self.points_entry = Spinbox(
            self.haut, textvariable=self.points_var, from_=0, to=100, width=4
        )
        self.points_entry.pack(side=RIGHT, padx=5)
        Label(self.haut, text="Points :").pack(side=RIGHT)

        self.milieu = Frame(self)
        self.milieu.pack(fill="x", expand=True, padx=10, pady=10)
        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM, fill="x", expand=True, pady=5)

        self.obligatoire_var = BooleanVar(value=obligatoire)
        obligatoire_ui = Checkbutton(
            self.bas, text="Requis", variable=self.obligatoire_var
        )
        obligatoire_ui.pack(side=LEFT, padx=10)

        delete_button = Button(
            self.bas,
            text=" ⤫ ",
            command=lambda: page_callback(CallbackCommand.DELETE, self),
            style="warning",
        )
        delete_button.pack(side=RIGHT, padx=2)

        duplicate_button = Button(
            self.bas,
            text=" D ",
            command=lambda: page_callback(CallbackCommand.DUPLICATE, self),
            style="info",
        )
        duplicate_button.pack(side=RIGHT, padx=2)

        self.btn_down = Button(
            self.bas,
            text=" 🠋 ",
            command=lambda: page_callback(CallbackCommand.MOVE_DOWN, self),
        )
        self.btn_down.pack(side=RIGHT, padx=2)

        self.btn_up = Button(
            self.bas,
            text=" 🠉 ",
            command=lambda: page_callback(CallbackCommand.MOVE_UP, self),
        )
        self.btn_up.pack(side=RIGHT, padx=2)

    def delete(self):
        raise NotImplementedError

    def duplicate(self):
        raise NotImplementedError
