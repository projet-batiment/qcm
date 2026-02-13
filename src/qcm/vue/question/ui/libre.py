from ttkbootstrap import Entry, Frame, StringVar

from qcm.model.question import QuestionLibre
from qcm.vue.parent import Parent

from .ui import QuestionUI


class QuestionLibreUI(QuestionUI):
    """
    Conteneur de l'interface graphique pour éditer une QuestionLibre
    du model.

    Attributes:
        question_type (str):
            Nom de ce type de question dans l'interface graphique.
    """

    question_type = "Question libre"

    def __init__(self, parent: Parent, question: QuestionLibre, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            question (QuestionLibre): la question du model à éditer
        """

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
        """
        Met à jour la vue selon les données en mémoire.
        """
        self.rep_attendue_var.set(self.question.rep_attendue)


# ajouter cette implémentation à la liste de la classe mère
QuestionUI.implementations.append(QuestionLibreUI)
