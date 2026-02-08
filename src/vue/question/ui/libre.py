from ttkbootstrap import Entry, Frame, StringVar

from model.question import QuestionLibre

from .ui import QuestionUI


class QuestionLibreUI(QuestionUI):
    question_type = "Question libre"

    def __init__(self, parent, question: QuestionLibre, *args, **kwargs):
        super().__init__(parent, question=question, *args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.rep_attendue_var = StringVar(value=question.rep_attendue)

        def rep_attendue_var_changed(*args):
            self.question.rep_attendue = self.rep_attendue_var.get()

        self.rep_attendue_var.trace_add("write", rep_attendue_var_changed)

        self.rep_attendue_entry = Entry(
            self.container, textvariable=self.rep_attendue_var
        )
        self.rep_attendue_entry.pack(fill="x")

        self.update()

    def update(self):
        self.rep_attendue_var.set(self.question.rep_attendue)


QuestionUI.implementations.append(QuestionLibreUI)
