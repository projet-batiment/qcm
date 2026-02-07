from tkinter import BOTTOM, LEFT, RIGHT, TOP
from ttkbootstrap import BooleanVar, Button, Checkbutton, Entry, Frame, StringVar

from model.question import QuestionQCMultiples

from .ui import QuestionUI

class QuestionQCMultiplesUI(QuestionUI):
    @staticmethod
    def question_type():
        return "Choix multiples"

    def __init__(self, parent, page_callback, question: QuestionQCMultiples, *args, **kwargs):
        super().__init__(parent, page_callback=page_callback, question=question, *args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.vars_texte = []
        self.vars_etat = []

        def add():
            self.question.choix_rep.append("Nouveau choix")
            self.update()

        add_button_container = Frame(self.container)
        add_button_container.pack(side=BOTTOM, expand=True, fill="x")
        add_button = Button(add_button_container, text="Ajouter", command=add)
        add_button.pack(side=LEFT)

        self.update()

    def update(self):
        for each_old_ui in self.choix_ui:
            each_old_ui.pack_forget()

        self.choix_ui = []
        self.vars_texte = []
        self.vars_etat = []

        for i, each_choix in enumerate(self.question.choix_rep):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            txt_var = StringVar(value=each_choix)
            self.vars_texte.append(txt_var)

            etat_var = BooleanVar(value=False)
            self.vars_etat.append(etat_var)

            each_check = Checkbutton(each_frame, variable=etat_var)
            each_check.pack(side=LEFT)

            each_entry = Entry(each_frame, textvariable=txt_var)
            each_entry.pack(side=LEFT)

            def delete(i=i):
                self.question.choix_rep.pop(i)
                self.update()

            Button(each_frame, text=" ⤫ ", command=delete, style="warning").pack(
                side=RIGHT
            )

            def move_down(i=i):
                self.question.choix_rep.insert(i + 1, self.question.choix_rep.pop(i))
                self.update()

            btn_down = Button(each_frame, text=" 🠋 ", command=move_down)
            btn_down.pack(side=RIGHT)
            if i + 1 == len(self.question.choix_rep):
                btn_down.config(state="disabled")

            def move_up(i=i):
                self.question.choix_rep.insert(i - 1, self.question.choix_rep.pop(i))
                self.update()

            btn_up = Button(each_frame, text=" 🠉 ", command=move_up)
            btn_up.pack(side=RIGHT)
            if i == 0:
                btn_up.config(state="disabled")

            self.choix_ui.append(each_frame)
