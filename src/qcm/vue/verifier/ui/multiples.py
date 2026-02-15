from tkinter import LEFT, TOP

from ttkbootstrap import BooleanVar, Checkbutton, Frame, Label

from qcm.model.question import QuestionQCMultiples
from qcm.vue.parent import Parent

from .ui import ReponseUI


class ReponseQCMultiplesUI(ReponseUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseQCMultiples
    du model.
    """

    def __init__(self, parent: Parent, question: QuestionQCMultiples, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            question (QuestionQCMultiples): la question du model à laquelle répondre
        """

        super().__init__(parent, question, *args, **kwargs)

        self.question = question

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.vars_etat = []

        self.checked = set()

        self.update()

    def update(self):
        """
        Met à jour la vue selon les données en mémoire.

        Fonctionnement: supprime tous les éléments graphiques puis
        les recrée avec les nouvelles valeurs.
        """

        for each_old_ui in self.choix_ui:
            each_old_ui.pack_forget()

        self.choix_ui = []
        self.vars_etat = []

        for i, each_choix in enumerate(self.question.choix_rep):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            etat_var = BooleanVar(value=False)
            self.vars_etat.append(etat_var)
            each_check = Checkbutton(each_frame, variable=etat_var)
            each_check.pack(side=LEFT)
            each_label = Label(each_frame, text=each_choix)
            each_label.pack(side=LEFT)

            self.choix_ui.append(each_frame)
