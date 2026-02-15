from ttkbootstrap import Frame, Label

from qcm.model.reponse import ReponseLibre
from qcm.vue.parent import Parent

from .ui import CorrectionUI


class CorrectionLibreUI(CorrectionUI):
    """
    Conteneur de l'interface graphique pour afficher la correction
    d'une ReponseLibre du model.
    """

    def __init__(self, parent: Parent, reponse: ReponseLibre, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            reponse (ReponseLibre): la reponse du model
        """

        super().__init__(parent, reponse, *args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)

        self.answer = Label(self.container)
        self.answer.pack(fill="x")

        self.correction = Label(self.container)

        self.update()

    def update(self):
        """
        Met à jour la vue selon les données en mémoire.
        """

        self.answer.config(text=f"Votre réponse : {self.reponse.reponse}")
        if self.reponse.verifier():
            self.correction.pack_forget()
        else:
            self.correction.config(
                text=f"Réponse attendue : {self.reponse.question.rep_attendue}"
            )
            self.correction.pack(fill="x")
