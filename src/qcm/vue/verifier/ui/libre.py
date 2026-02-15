from ttkbootstrap import Entry, Frame, StringVar

from qcm.model.question import QuestionLibre
from qcm.vue.parent import Parent

from .ui import ReponseUI


class ReponseLibreUI(ReponseUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseLibre
    du model.
    """

    def __init__(self, parent: Parent, question: QuestionLibre, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            question (QuestionLibre): la question du model à laquelle répondre
        """

        super().__init__(parent, question, *args, **kwargs)

        self.question = question

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_var = StringVar(value="")
        self.answer = Entry(self.container, textvariable=self.choix_var)
        self.answer.pack(fill="x")

        self.update()

    def update(self):
        """
        Met à jour la vue selon les données en mémoire.
        """
        self.choix_var.set("")
