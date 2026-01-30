from ttkbootstrap import Frame, Button
from ttkbootstrap.scrolled import ScrolledFrame
import logging

from vue.editeur.editeur_callback_type import CallbackCommand

from vue.editeur.choix_unique import ChoixUnique
from vue.editeur.editeur import Editeur

class EditeurPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.questions = []

        self.btn_ajouter = Button(
            self,
            text="➕ Ajouter une nouvelle question",
            command=self.ajouter_question,
            style="info"
        )
        self.btn_ajouter.pack(pady=10)

        self.scroll_container = ScrolledFrame(self, autohide=True)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.ajouter_question()

    def _editeur_callback(self, command: CallbackCommand, question: Editeur):
        try:
            question_index = self.questions.index(question)
        except ValueError as e:
            logging.error("question not found in the list")
            raise e

        match command:
            case CallbackCommand.DELETE:
                question.pack_forget()
                self.questions.pop(question_index)

            case CallbackCommand.DUPLICATE:
                raise NotImplementedError

            case CallbackCommand.MOVE_UP:
                if (question_index > 0):
                    self.questions.insert(question_index-1, self.questions.pop(question_index))

            case CallbackCommand.MOVE_DOWN:
                if (question_index+1 < len(self.questions)):
                    self.questions.insert(question_index+1, self.questions.pop(question_index))

        self.update_questions_view()

    def update_questions_view(self):
        for each in self.questions:
            each.pack_forget()
            each.pack(fill="x", pady=10)

    def ajouter_question(self):
        self.questions.append(ChoixUnique(
            self.scroll_container,
            page_callback=self._editeur_callback,
        ))

        self.update_questions_view()
