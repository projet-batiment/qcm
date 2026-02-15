from tkinter import LEFT, TOP

from ttkbootstrap import Frame, IntVar, Label, Radiobutton

from qcm.model.question import QuestionQCUnique

from .ui import ReponseUI


class ReponseQCUniqueUI(ReponseUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseQCUnique
    du model.
    """

    def __init__(self, parent, question: QuestionQCUnique, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            question (QuestionQCUnique): la question du model à laquelle répondre
        """

        super().__init__(parent, question, *args, **kwargs)

        self.question = question

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.choix_ui = []
        self.choix_var = IntVar(value=-1)

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

        for i, each_choix in enumerate(self.question.choix_rep):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            each_radio = Radiobutton(each_frame, value=i, variable=self.choix_var)
            each_radio.pack(side=LEFT)
            each_label = Label(each_frame, text=each_choix)
            each_label.pack(side=LEFT)

            self.choix_ui.append(each_frame)
