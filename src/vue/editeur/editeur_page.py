from ttkbootstrap import Frame, Button
from ttkbootstrap.scrolled import ScrolledFrame

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
        nouvelle = ChoixUnique(self.scroll_container)
        nouvelle.pack(fill="x", pady=10)

        self.questions.append(nouvelle)
