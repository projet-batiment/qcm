from logging import getLogger
from typing import TYPE_CHECKING

from ttkbootstrap import Button, Entry, Frame, StringVar
from ttkbootstrap.scrolled import ScrolledFrame

from qcm.model.reponse import (
    Reponse,
    ReponseLibre,
    ReponseQCMultiples,
    ReponseQCUnique,
)
from qcm.model.tentative import Tentative
from qcm.vue.parent import Parent

from .ui import ReponseLibreUI, ReponseQCMultiplesUI, ReponseQCUniqueUI

if TYPE_CHECKING:
    from qcm.control.controller import Control

logger = getLogger(__name__)


class MainView(Frame):
    """
    Conteneur premier niveau pour le mode Remplissage de Tentative.
    N'est instanciée qu'une seule fois par exécution.
    """

    def __init__(self, parent: Parent, controller: "Control"):
        """
        Args:
            parent (Parent): the parent container
            controller (Control): the app controller
        """

        super().__init__(parent, width=800)
        self.pack_propagate(False)

        self.controller = controller

        self.nom_var = StringVar()

        def nom_var_changed(*args):
            self.tentative.nom = self.nom_var.get()

        self.nom_var.trace_add("write", nom_var_changed)

        self.nom = Entry(self, textvariable=self.nom_var)
        self.nom.pack(pady=10)

        self.reponses_ui = []

        self.scroll_outer = ScrolledFrame(self, autohide=True)
        self.scroll_outer.pack(fill="both", expand=True, padx=20, pady=20)
        self.scroll_container = Frame(self.scroll_outer)
        self.scroll_container.pack(fill="both", expand=True, padx=(0, 10))

        self.btn_valider = Button(
            self.scroll_container,
            text="✅ Envoyer",
            command=self.controller.verifier_tentative,
            style="info",
        )

    def update_view(self):
        """
        Met à jour la vue selon les données en mémoire.

        Fonctionnement: supprime tous les éléments graphiques puis
        les recrée avec les nouvelles valeurs.
        """

        self.nom_var.set(self.tentative.nom)

        for reponse_ui in self.reponses_ui:
            reponse_ui.pack_forget()
        self.btn_valider.pack_forget()

        self.reponses_ui = []
        for reponse in self.tentative.liste_reponses:
            self.__open_reponse(reponse)
        self.btn_valider.pack(pady=20)

    def __open_reponse(self, reponse: Reponse) -> None:
        """
        Crée l'interface (.ui.ReponseUI) correspondant à la reponse
        model donnée en argument, puis l'ajoute à la liste des interfaces.

        Args:
            reponse (Reponse): reponse (model) à afficher
        """

        ui_class = None

        match reponse:
            case ReponseQCUnique():
                ui_class = ReponseQCUniqueUI

            case ReponseQCMultiples():
                ui_class = ReponseQCMultiplesUI

            case ReponseLibre():
                ui_class = ReponseLibreUI

            case _:
                raise ValueError(
                    f"Unsupported reponse type of class '{reponse.__class__.__name__}'"
                )

        reponse_ui = ui_class(
            self.scroll_container,
            reponse=reponse,
        )
        reponse_ui.pack(fill="x", pady=10)
        self.reponses_ui.append(reponse_ui)

    def set_tentative(self, tentative: Tentative) -> None:
        """
        Remplace la tentative actuelle et son contenu par la tentative
        donnée en argument.

        Args:
            tentative (Tentative): la tentative à ouvrir
        """

        logger.info(f"Opening tentative '{tentative.nom}'")
        self.tentative = tentative

        for i, reponse in enumerate(tentative.liste_reponses):
            try:
                self.__open_reponse(reponse)
            except ValueError as e:
                logger.error(f"Failed to open reponse #{i}: {e}")

        self.update_view()
