from tkinter import LEFT, TOP

from ttkbootstrap import BooleanVar, Checkbutton, Frame, Label

from qcm.model.reponse import ReponseQCMultiples
from qcm.vue.parent import Parent

from .qcm import CorrectionQCUI


class CorrectionQCMultiplesUI(CorrectionQCUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseQCMultiples
    du model.
    """

    def __init__(self, parent: Parent, reponse: ReponseQCMultiples, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            reponse (ReponseQCMultiples): la reponse du model
        """

        super().__init__(parent=parent, reponse=reponse, *args, **kwargs)

        self.choix_ui = []
        self.vars_etat = []

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

        for i, each_choix in enumerate(self.reponse.question.choix):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            etat_var = BooleanVar(value=i in self.reponse.reponses_choisies)
            self.vars_etat.append(etat_var)

            corr_var = BooleanVar(
                value=i in self.reponse.question.index_bonnes_reponses
            )
            self.vars_etat.append(corr_var)

            each_check = Checkbutton(each_frame, variable=etat_var)
            each_check.pack(side=LEFT)
            each_check.config(state="disabled")

            each_label = Label(each_frame, text=each_choix)
            each_label.pack(side=LEFT)

            each_check_corr = Checkbutton(each_frame, variable=corr_var)
            each_check_corr.pack(side="right")
            each_check_corr.config(state="disabled")

            self.choix_ui.append(each_frame)
