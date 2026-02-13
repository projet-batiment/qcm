from tkinter import BOTTOM, LEFT, RIGHT, TOP

from ttkbootstrap import BooleanVar, Button, Checkbutton, Entry, Frame, StringVar

from qcm.model.question import QuestionQCMultiples

from .ui import QuestionUI


class QuestionQCMultiplesUI(QuestionUI):
    question_type = "Choix multiples"

    def __init__(
        self, parent, page_callback, question: QuestionQCMultiples, *args, **kwargs
    ):
        super().__init__(
            parent, page_callback=page_callback, question=question, *args, **kwargs
        )

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.vars_texte = []
        self.vars_etat = []

        def add():
            self.question.choix.append("Nouveau choix")
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

        for i, each_choix in enumerate(self.question.choix):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            etat_var = BooleanVar(value=i in self.question.index_bonnes_reponses)

            def check_value_updated(*args, i=i, etat_var=etat_var):
                self.question.set_bonne_reponse(i, etat_var.get())

            etat_var.trace_add("write", check_value_updated)
            self.vars_etat.append(etat_var)

            each_check = Checkbutton(each_frame, variable=etat_var)
            each_check.pack(side=LEFT)

            each_var = StringVar(value=each_choix)

            def entry_text_updated(*args, i=i, each_var=each_var):
                self.question.choix[i] = each_var.get()

            each_var.trace_add("write", entry_text_updated)
            self.vars_texte.append(each_var)

            each_entry = Entry(each_frame, textvariable=each_var)
            each_entry.pack(side=LEFT)

            def delete(i=i):
                self.question.delete_choix(i)
                self.update()

            Button(each_frame, text=" ⤫ ", command=delete, style="warning").pack(
                side=RIGHT
            )

            def move_down(i=i):
                self.question.swap_choix(i, i + 1)
                self.update()

            btn_down = Button(each_frame, text=" 🠋 ", command=move_down)
            btn_down.pack(side=RIGHT)
            if i + 1 == len(self.question.choix):
                btn_down.config(state="disabled")

            def move_up(i=i):
                self.question.swap_choix(i, i - 1)
                self.update()

            btn_up = Button(each_frame, text=" 🠉 ", command=move_up)
            btn_up.pack(side=RIGHT)
            if i == 0:
                btn_up.config(state="disabled")

            self.choix_ui.append(each_frame)


QuestionUI.implementations.append(QuestionQCMultiplesUI)
