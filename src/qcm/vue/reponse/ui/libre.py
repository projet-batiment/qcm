from ttkbootstrap import Entry, Frame, StringVar

from qcm.model.reponse import ReponseLibre
from qcm.vue.parent import Parent

from .ui import ReponseUI


class ReponseLibreUI(ReponseUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseLibre
    du model.
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

        def reponse_var_changed(*args):
            self.reponse.reponse = self.reponse_var.get()

        self.reponse_var = StringVar(value="")
        self.reponse_var.trace_add("write", reponse_var_changed)

        self.answer = Entry(self.container, textvariable=self.reponse_var)
        self.answer.pack(fill="x")

        self.update()

    def update(self):
        """
        Met à jour la vue selon les données en mémoire.
        """
        self.reponse_var.set(self.reponse.reponse)
