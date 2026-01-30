from ttkbootstrap import Frame, Button
from ttkbootstrap.scrolled import ScrolledFrame
import logging

from vue.editeur.choix_unique import ChoixUnique

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

    def ajouter_question(self):
        index = len(self.questions)

        nouvelle = ChoixUnique(
            self.scroll_container,
            delete_callback=self.supprimer_question,
            duplicate_callback=lambda: NotImplemented,
        )
        nouvelle.pack(fill="x", pady=10)

        self.questions.append(nouvelle)

    def supprimer_question(self, question):
        question.pack_forget()
        try:
            self.questions.pop(self.questions.index(question))
        except ValueError:
            logging.error("question not found in the list")
