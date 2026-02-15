from tkinter import LEFT, TOP

from ttkbootstrap import Frame, IntVar, Label, Radiobutton

from qcm.model.reponse import ReponseQCUnique

from .qcm import CorrectionQCUI


class CorrectionQCUniqueUI(CorrectionQCUI):
    """
    Conteneur de l'interface graphique pour éditer une ReponseQCUnique
    du model.
    """

    def __init__(self, parent, reponse: ReponseQCUnique, *args, **kwargs):
        """
        Args:
            parent (Parent): conteneur parent
            reponse (ReponseQCUnique): la reponse du model
        """

        super().__init__(parent=parent, reponse=reponse, *args, **kwargs)

        self.choix_ui = []
        self.choix_var = IntVar(value=self.reponse.reponse_choisie)
        self.corr_var = IntVar(value=self.reponse.question.index_bonne_reponse)

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

        for i, each_choix in enumerate(self.reponse.question.choix):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            each_radio = Radiobutton(each_frame, value=i, variable=self.choix_var)
            each_radio.config(state="disabled")
            each_radio.pack(side=LEFT)
            each_label = Label(each_frame, text=each_choix)
            each_label.pack(side=LEFT)

            each_radio_corr = Radiobutton(each_frame, value=i, variable=self.corr_var)
            each_radio_corr.config(state="disabled")
            each_radio_corr.pack(side="right")

            self.choix_ui.append(each_frame)
