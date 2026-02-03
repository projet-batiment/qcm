from ttkbootstrap import Frame, Entry, Radiobutton, IntVar, Button, StringVar, Label
from tkinter import LEFT, TOP, RIGHT, BOTTOM

from model.question import QuestionLibre
from .ui import ReponseUI

class ReponseLibreUI(ReponseUI):
    def __init__(self, parent, question: QuestionLibre, *args, **kwargs):
        super().__init__(parent, question, *args, **kwargs)

        self.question = question

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_var = StringVar(value="")
        self.answer = Entry(self.container, textvariable=self.choix_var)
        self.answer.pack(fill="x")

        self.update()

    def update(self):
        self.choix_var.set("")
