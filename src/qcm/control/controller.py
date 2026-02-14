import logging
from tkinter import filedialog, messagebox
from ttkbootstrap import Frame, Window

from typing import Optional

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

        self.states = {
            AppState.SPLASH_SCREEN: splashscreen.MainView(window),
            AppState.EDIT: question.MainView(window),
        }
        self.__current_state: Optional[Frame] = None
        self.appstate: AppState = AppState.SPLASH_SCREEN

        self.menubar = MenuBar(window, self)
        window.config(menu=self.menubar)

        self.qcm: Optional[Qcm] = None         # qcm affiché dans l'interface
        self.filename: Optional[str] = None    # fichier de sauvegarde du qcm

    @property
    def qcm(self) -> Optional[Qcm]:
        return self.__qcm

    @qcm.setter
    def qcm(self, qcm: Optional[Qcm]) -> None:
        self.__qcm = qcm

        if qcm is None:
            logger.debug("Setting qcm to None")
            self.menubar.has_qcm(False)
            self.appstate = AppState.SPLASH_SCREEN
        else:
            logger.debug(f"Setting qcm to '{qcm.titre}'")
            self.menubar.has_qcm(True)

    @property
    def appstate(self) -> Optional[AppState]:
        """
        Renvoie l'état actuel de l'interface.

        Returns:
            Optional[AppState]:
                L'état ou None s'il n'est pas trouvé dans la liste des états
        """
        return next((k for k, v in self.states.items() if v == self.__current_state), None)

    @appstate.setter
    def appstate(self, appstate: AppState) -> None:
        """
        Permet de changer le mode de la vue
        Voir aussi les modes dans AppState

        Args:
            appstate (AppState): le nouvel état

        Raises:
            ValueError: l'état requis est inconnu
        """

        logger.debug(f"Setting appstate {appstate}")
        if appstate not in self.states:
            raise ValueError(f"Not a known state: {appstate}")

        if self.__current_state is not None:
            self.__current_state.pack_forget()

        self.__current_state = self.states[appstate]
        self.__current_state.pack(fill="both", expand=True)

    def new_file(self) -> None:
        """
        Créer un nouveau qcm et l'afficher en édition
        """

        logger.debug("Creating new qcm")

        self.qcm = Qcm()
        self.states[AppState.EDIT].set_qcm(self.qcm)
        self.appstate = AppState.EDIT

    def open_file(self) -> None:
        """
        Ouvrir un qcm depuis un fichier l'afficher en édition
        """

        if self.qcm is not None and not self.__ask_save_file_and_close():
            return

        logger.debug("Asking filename for opennig qcm")
        filename = filedialog.askopenfilename(
            title="Ouvrir...",
            **askfilename_options,
        )

        if len(filename) == 0:
            logger.debug("User cancelled operation...")
            return

        self.filename = filename
        logger.debug(f"Opening qcm from file {self.filename}")

        try:
            self.qcm = read_from_file(filename)
            self.states[AppState.EDIT].set_qcm(self.qcm)
            self.appstate = AppState.EDIT

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

    def save_file_as(self) -> bool:
        """
        Sauvegarder le qcm actuellement édité vers un
        fichier choisi interactivement.

        Returns:
            bool:
                True si sauvegardé
                False si annulé
        """

        logger.debug("Asking filename for saving qcm as")
        filename = filedialog.asksaveasfilename(
            title="Enregistrer sous...",
            **askfilename_options,
        )

        if len(filename) == 0:
            logger.debug("User cancelled operation...")
            return False

        self.filename = filename
        self.save_file()

        return True

    def save_file(self) -> bool:
        """
        Sauvegarder le qcm actuellement édité vers le fichier actuel.
        Demande le fichier à enregistrer s'il n'y en a pas en mémoire.

        Returns:
            bool:
                True si sauvegardé
                False si annulé ou erreur
        """

        if self.filename is None:
            return self.save_file_as()

        else:
            logger.debug(f"Saving qcm to file {self.filename}")

            try:
                save_to_file(self.qcm, self.filename)

                messagebox.showinfo(
                    title="Sauvegarde réussie",
                    message=f"Le qcm a bien été enregistré dans le fichier"
                    f"'{self.filename}.'",
                )

                return True

            except Exception as e:
                messagebox.showerror(
                    title="Sauvegarde impossible",
                    message=f"Erreur lors de la sauvegarde du fichier: {e}",
                )

                return False

    def close_qcm(self) -> None:
        """
        Ferme le qcm actuellement édité.
        """

        self.__ask_save_file_and_close()

    def __ask_save_file_and_close(self) -> bool:
        """
        Demdande cnofirmation pour le fichier avant fermeture.
        Puis ferme le qcm actuel.

        Returns:
            bool:
                True si continuer (boutons oui ou non choisis)
                False si annuler (ne pas faire les actions suivantes)
        """

        answer = messagebox.askyesnocancel(
            title="Confirmation",
            message="Voulez-vous enregistrer le qcm avant la fermeture ? "
                    "Les modifications non-sauvegardées "
                    "pourraient être perdues.",
        )

        match answer:
            case True:
                logger.debug("Enregistrement du qcm avant fermeture")
                proceed = self.save_file()

            case False:
                logger.debug("Fermeture du qcm sans enregistrement")
                proceed = True

            case None:
                proceed = False

        if proceed:
            logger.debug("Fermeture du qcm")
            self.qcm = None
        else:
            logger.info("Annulation de la fermeture du qcm...")

        return proceed
