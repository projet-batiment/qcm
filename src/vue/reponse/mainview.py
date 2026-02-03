from ttkbootstrap import Frame, Button, Label, StringVar
from ttkbootstrap.scrolled import ScrolledFrame

from logging import warning

from model.qcm import Qcm
from model import question

from .ui import ReponseQCUniqueUI, ReponseQCMultiplesUI, ReponseLibreUI

class MainView(Frame):
    def __init__(self, parent, qcm: Qcm):
        super().__init__(parent, width=800)
        self.pack_propagate(False)

        self.qcm = qcm

        self.titre = Label(self, text=qcm.titre)
        self.titre.pack(pady=10)

        self.scroll_outer = ScrolledFrame(self, autohide=True)
        self.scroll_outer.pack(fill="both", expand=True, padx=20, pady=20)
        self.scroll_container = Frame(self.scroll_outer)
        self.scroll_container.pack(fill="both", expand=True, padx=(0, 10))

        self.reponse_uis = []

        self.btn_valider = Button(
            self.scroll_container,
            text="✅ Envoyer",
            command=self.valider,
            style="info"
        )

        self.update_view()

    def update_view(self):
        for each in self.reponse_uis:
            each.pack_forget()

        self.reponse_uis = []
        self.btn_valider.pack_forget()

        for each_question in self.qcm.liste_questions:
            match each_question:
                case question.QuestionQCUnique():
                    each_reponse = ReponseQCUniqueUI(self.scroll_container, each_question)

                case question.QuestionQCMultiples():
                    each_reponse = ReponseQCMultiplesUI(self.scroll_container, each_question)

                case question.QuestionLibre():
                    each_reponse = ReponseLibreUI(self.scroll_container, each_question)

                case _:
                    raise NotImplementedError
                    continue

            self.reponse_uis.append(each_reponse)
            each_reponse.pack(fill="x", pady=10)

        self.btn_valider.pack(pady=20)

    def valider(self):
        raise NotImplementedError
