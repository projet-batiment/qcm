from tkinter import BOTTOM, LEFT, RIGHT, TOP

from ttkbootstrap import Button, Entry, Frame, IntVar, Radiobutton, StringVar

from qcm.model.question import QuestionQCUnique

from .ui import QuestionUI


class QuestionQCUniqueUI(QuestionUI):
    question_type = "Choix unique"

    def __init__(self, parent, question: QuestionQCUnique, *args, **kwargs):
        super().__init__(parent, question=question, *args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.choix_var = IntVar(value=-1)
        self.vars = []

        def choix_var_changed(*args):
            self.question.id_bonne_reponse = self.choix_var.get()

        self.choix_var.trace_add("write", choix_var_changed)

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
        self.vars = []

        self.choix_var.set(self.question.id_bonne_reponse)

        for i, each_choix in enumerate(self.question.choix_rep):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            each_radio = Radiobutton(each_frame, value=i, variable=self.choix_var)
            each_radio.pack(side=LEFT)

            each_var = StringVar(value=each_choix)

            def entry_text_updated(*args, i=i, each_var=each_var):
                self.question.choix_rep[i] = each_var.get()

            each_var.trace_add("write", entry_text_updated)
            self.vars.append(each_var)

            each_entry = Entry(each_frame, textvariable=each_var)
            each_entry.pack(side=LEFT)

            def delete(i=i):
                self.question.choix_bdd.pop(i)
                self.update()

            each_delete = Button(
                each_frame, text=" ⤫ ", command=delete, style="warning"
            )
            each_delete.pack(side=RIGHT)

            def move_down(i=i):
                self.question.choix_bdd.insert(i + 1, self.question.choix_bdd.pop(i))
                self.update()

            each_move_down = Button(each_frame, text=" 🠋 ", command=move_down)
            each_move_down.pack(side=RIGHT)
            if i + 1 == len(self.question.choix_bdd):
                each_move_down.config(state="disabled")

            def move_up(i=i):
                self.question.choix_bdd.insert(i - 1, self.question.choix_bdd.pop(i))
                self.update()

            each_move_up = Button(each_frame, text=" 🠉 ", command=move_up)
            each_move_up.pack(side=RIGHT)
            if i == 0:
                each_move_up.config(state="disabled")

            self.choix_ui.append(each_frame)


QuestionUI.implementations.append(QuestionQCUniqueUI)
