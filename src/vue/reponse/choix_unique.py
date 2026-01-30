from ttkbootstrap import Frame, Entry, Radiobutton, IntVar, Button, StringVar, Label
from tkinter import LEFT, TOP, RIGHT, BOTTOM

from model.question import QuestionQCUnique
from .reponse_ui import ReponseUI

class ReponseQCUniqueUI(ReponseUI):
    def __init__(self, parent, question: QuestionQCUnique, *args, **kwargs):
        super().__init__(parent, question, *args, **kwargs)

        self.question = question

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.choix_var = IntVar(value=-1)

        self.update()

    def update(self):
        for each_old_ui in self.choix_ui:
            each_old_ui.pack_forget()

        self.choix_ui = []

        for i, each_choix in enumerate(self.question.choix_rep):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            each_radio = Radiobutton(each_frame, value=i, variable=self.choix_var)
            each_radio.pack(side=LEFT)
            each_label = Label(each_frame, text=each_choix)
            each_label.pack(side=LEFT)

            self.choix_ui.append(each_frame)
