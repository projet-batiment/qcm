from __future__ import annotations

from tkinter import BOTTOM, LEFT, RIGHT, TOP

from ttkbootstrap import (
    BooleanVar,
    Button,
    Checkbutton,
    Combobox,
    Entry,
    Frame,
    IntVar,
    Label,
    Spinbox,
    StringVar,
)

from qcm.model.question import Question

from ..callback_type import CallbackCommand


class QuestionUI(Frame):
    # NOTE: question_type n'est plus une fonction statique puisque
    #  cela complique pour un rien la logique et la lourdeur de
    #  l'exécution dans mainview alors qu'avec un simple attribut
    #  il n'y a aucune complication.
    #  Certes c'est moins propre car on a pas de décorateur.
    #  Mais au moins c'est pas boilerplate.
    #  Et puis python avait qu'à avoir un décorateur abstractattribute aussi !!

    implementations: list[QuestionUI] = []

    def __init__(
        self,
        parent,
        page_callback,
        question: Question,
    ):
        super().__init__(parent, width=600, borderwidth=2, relief="solid")

        self.question = question

        self.haut = Frame(self)
        self.haut.pack(side=TOP, fill="x", expand=True, pady=5)

        def titre_var_changed(*args):
            self.question.enonce = self.titre_var.get()

        self.titre_var = StringVar(value=question.enonce)
        self.titre_var.trace_add("write", titre_var_changed)

        self.titre_entry = Entry(self.haut, textvariable=self.titre_var, width=40)
        self.titre_entry.pack(side=LEFT, padx=5)

        # NOTE: self.question_type: voir note en haut de classe
        self.type_var = StringVar(value=self.question_type)
        self.type_selector = Combobox(
            self.haut,
            textvariable=self.type_var,
            values=[x.question_type for x in self.implementations],
            state="readonly",
            width=15,
        )
        self.type_selector.pack(side=LEFT, padx=10)
        self.type_selector.bind(
            "<<ComboboxSelected>>",
            lambda e: page_callback(CallbackCommand.CHANGE_TYPE, self),
        )

        self.points_var = IntVar(value=question.points)
        self.points_entry = Spinbox(
            self.haut, textvariable=self.points_var, from_=0, to=100, width=4
        )
        self.points_entry.pack(side=RIGHT, padx=5)
        Label(self.haut, text="Points :").pack(side=RIGHT)

        self.milieu = Frame(self)
        self.milieu.pack(fill="x", expand=True, padx=10, pady=10)
        self.bas = Frame(self)
        self.bas.pack(side=BOTTOM, fill="x", expand=True, pady=5)

        def obligatoire_var_changed(*args):
            # TODO: le model n'implémente pas l'infomation "requis/obligatoire"
            raise NotImplementedError

        self.obligatoire_var = BooleanVar(value=True)
        self.obligatoire_var.trace_add("write", obligatoire_var_changed)
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
