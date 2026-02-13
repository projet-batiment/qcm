from logging import info
from ttkbootstrap import Frame, Window

from qcm.control import AppState
from qcm.vue import MenuBar, question, splashscreen


class Control:
    """
    Gère les opérations logiques appliquées à la vue.
    N'est instanciée qu'une seule fois par exécution.
    """

    def __init__(self, window: Window) -> "Control":
        """
        Args:
            window (Window): fenêtre principale de l'application
        """

        self.appstate = AppState.SPLASH_SCREEN

        self.states = {
            AppState.SPLASH_SCREEN: splashscreen.MainView(window),
            AppState.EDIT: question.MainView(window),
        }

        window.config(menu=MenuBar(window, self))

        self.current_state: Frame = None
        self.set_appstate(AppState.SPLASH_SCREEN)

    def set_appstate(self, appstate: AppState) -> None:
        """
        Permet de changer le mode de la vue
        Voir aussi les modes dans AppState

        Args:
            appstate (AppState): le nouvel état
        """

        if appstate not in self.states:
            raise ValueError(f"Not a known state: {appstate}")

        if self.current_state is not None:
            self.current_state.pack_forget()

        self.current_state = self.states[appstate]
        self.current_state.pack(fill="both", expand=True)

    def new_file(self) -> None:
        """
        Créer un nouveau qcm et l'afficher en édition
        """

        self.set_appstate(AppState.EDIT)
        self.states[AppState.EDIT].set_qcm_new()

    def open_file(self) -> None:
        """
        Ouvrir un qcm depuis un fichier l'afficher en édition
        """

        info("ouvrir qcm")

    def save_file(self) -> None:
        """
        Sauvegarder le qcm actuellement édité vers un fichier
        """

        info("sauvegarder qcm")
