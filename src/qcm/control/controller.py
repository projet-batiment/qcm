import logging
from tkinter import filedialog, messagebox

from ttkbootstrap import Frame, Window

from qcm.control.appstate import AppState
from qcm.control.db_manager import read_from_file, save_to_file
from qcm.model.qcm import Qcm
from qcm.vue import MenuBar, question, splashscreen

logger = logging.getLogger(__name__)

# default Tkinter.filedialog.* arguments
askfilename_options = {
    "defaultextension": ".qdb",
    "filetypes": [("Ficher QCM", "*.qdb"), ("Tous les fichiers", "*.*")],
}


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

        self.qcm = Qcm()
        self.filename = None

        self.current_state: Frame = None
        self.set_appstate(AppState.SPLASH_SCREEN)

    def set_appstate(self, appstate: AppState) -> None:
        """
        Permet de changer le mode de la vue
        Voir aussi les modes dans AppState

        Args:
            appstate (AppState): le nouvel état
        """

        logger.debug(f"Setting appstate {appstate}")
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

        logger.debug("Creating new qcm")

        self.qcm = Qcm()
        self.states[AppState.EDIT].set_qcm(self.qcm)
        self.set_appstate(AppState.EDIT)

    def open_file(self) -> None:
        """
        Ouvrir un qcm depuis un fichier l'afficher en édition
        """

        logger.debug("Asking filename for opennig qcm")

        filename = filedialog.askopenfilename(
            title="Ouvrir...",
            **askfilename_options,
        )

        if filename == ():
            logger.debug("User cancelled operation...")
            return

        self.filename = filename
        logger.debug(f"Opening qcm from file {self.filename}")

        try:
            self.qcm = read_from_file(filename)
            self.states[AppState.EDIT].set_qcm(self.qcm)
            self.set_appstate(AppState.EDIT)

        except AttributeError:
            messagebox.showerror(
                title="Lecture impossible",
                message="La base de données du fichier spécifié est erronée.",
            )
        except Exception as e:
            messagebox.showerror(
                title="Lecture impossible",
                message=f"Erreur lors de l'ouverture du fichier: {e}",
            )

    def save_file_as(self) -> None:
        """
        Sauvegarder le qcm actuellement édité vers un fichier choisi interactivement.
        """

        logger.debug("Asking filename for saving qcm as")

        filename = filedialog.asksaveasfilename(
            title="Enregistrer sous...",
            **askfilename_options,
        )

        if filename == ():
            logger.debug("User cancelled operation...")
            return

        self.filename = filename
        self.save_file()

    def save_file(self) -> None:
        """
        Sauvegarder le qcm actuellement édité vers le fichier actuel.
        Demande le fichier à enregistrer s'il n'y en a pas en mémoire.
        """

        if self.filename is None:
            self.save_file_as()

        else:
            logger.debug(f"Saving qcm to file {self.filename}")

            try:
                save_to_file(self.qcm, self.filename)

                messagebox.showinfo(
                    title="Sauvegarde réussie",
                    message=f"Le qcm a bien été enregistré dans le fichier"
                    f"'{self.filename}.'",
                )

            except Exception as e:
                messagebox.showerror(
                    title="Sauvegarde impossible",
                    message=f"Erreur lors de la sauvegarde du fichier: {e}",
                )
