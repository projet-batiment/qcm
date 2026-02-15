import logging
from tkinter import filedialog, messagebox
from typing import Optional

from ttkbootstrap import Frame, Window

from qcm.control.appstate import AppState
from qcm.control.db_manager import read_from_file, save_to_file
from qcm.model.data import QcmData
from qcm.model.qcm import Qcm
from qcm.model.tentative import Tentative
from qcm.vue import MenuBar, question, reponse, splashscreen, verifier

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
            AppState.ANSWER: reponse.MainView(window, self),
            AppState.CORRECTION: verifier.MainView(window),
        }
        self.__current_state: Optional[Frame] = None
        self.appstate: AppState = AppState.SPLASH_SCREEN

        self.menubar = MenuBar(window, self)
        window.config(menu=self.menubar)

        self.qcm: Optional[Qcm] = None  # qcm affiché dans l'interface
        self.tentative: Optional[Tentative] = (
            None  # tentative affichée dans l'interface
        )
        self.filename: Optional[str] = None  # fichier de sauvegarde du qcm

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
    def tentative(self) -> Optional[Tentative]:
        return self.__tentative

    @tentative.setter
    def tentative(self, tentative: Optional[Tentative]) -> None:
        """
        Raises:
            ValueError: raised in case "self.qcm != tentative.qcm"
        """
        self.__tentative = tentative

        if tentative is None:
            logger.debug("Setting tentative to None")
            # TODO: menubar.has_tentative
            self.menubar.has_tentative(False)
            self.appstate = AppState.SPLASH_SCREEN
        else:
            if self.qcm != tentative.qcm:
                # Les étapes précédentes du controller assurent
                #   que self.qcm == tentative.qcm
                raise ValueError(
                    f"Expected self.qcm to already be set"
                    f" to tentative.qcm: '{self.qcm.titre}'"
                    f" != '{tentative.qcm.titre}'"
                )

            logger.debug(f"Setting tentative to '{tentative.nom}'")
            # TODO: menubar.has_tentative
            self.menubar.has_tentative(True)

    @property
    def tentatives(self):
        # TODO: temporary fix (only 1 Tentative for now)
        return [] if self.tentative is None else [self.tentative]

    @property
    def appstate(self) -> Optional[AppState]:
        """
        Renvoie l'état actuel de l'interface.

        Returns:
            Optional[AppState]:
                L'état ou None s'il n'est pas trouvé dans la liste des états
        """
        return next(
            (k for k, v in self.states.items() if v == self.__current_state), None
        )

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

    def new_qcm(self) -> None:
        """
        Créer un nouveau qcm et l'afficher en édition
        """

        logger.debug("Creating new qcm")

        self.qcm = Qcm()
        self.states[AppState.EDIT].set_qcm(self.qcm)
        self.appstate = AppState.EDIT

    def open_qcm(self) -> bool:
        """
        Ouvrir un qcm depuis un fichier l'afficher en édition

        Returns:
            bool:
                True si qcm effectivement ouvert
                False si annulé ou erreur
        """

        if self.qcm is not None and not self.__ask_save_qcm_and_close():
            return False

        logger.debug("Asking filename for opennig qcm")
        filename = filedialog.askopenfilename(
            title="Ouvrir...",
            **askfilename_options,
        )

        if len(filename) == 0:
            logger.debug("User cancelled operation...")
            return False

        self.filename = filename
        logger.debug(f"Opening qcm from file {self.filename}")

        try:
            data = read_from_file(filename)
            self.qcm = data.qcm

            # TODO: plusieurs tentatives ?
            self.tentative = next(iter(data.tentatives), None)

            self.states[AppState.EDIT].set_qcm(self.qcm)
            self.appstate = AppState.EDIT

            return True

        except AttributeError:
            messagebox.showerror(
                title="Lecture impossible",
                message="La base de données du fichier spécifié est erronée.",
            )

            return False

        except Exception as e:
            messagebox.showerror(
                title="Lecture impossible",
                message=f"Erreur lors de l'ouverture du fichier: {e}",
            )

            logger.exception("Erreur lors de l'ouverture du fichier")

            return False

    def save_qcm_as(self) -> bool:
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
        self.save_qcm()

        return True

    def save_qcm(self) -> bool:
        """
        Sauvegarder le qcm actuellement édité vers le fichier actuel.
        Demande le fichier à enregistrer s'il n'y en a pas en mémoire.

        Returns:
            bool:
                True si sauvegardé
                False si annulé ou erreur
        """

        if self.filename is None:
            return self.save_qcm_as()

        else:
            logger.debug(f"Saving qcm to file {self.filename}")

            try:
                data = QcmData(self.qcm, self.tentatives)
                save_to_file(data, self.filename)

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

        self.__ask_save_qcm_and_close()

    def __ask_save_qcm_and_close(self) -> bool:
        """
        Demande confirmation pour enregistrer le fichier avant fermeture.
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
                proceed = self.save_qcm()

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

    def start_tentative(self) -> bool:
        """
        Commencer une tentative pour un qcm.
        Vérifie si un qcm est déjà ouvert, sinon en ouvre un.
        Vérifie également la cohérence (si on peut répondre aux questions).

        Returns:
            bool:
                True si tentative effectivement commencée
                False si annulé ou erreur
        """

        if self.qcm is not None or self.open_qcm():
            if len(self.qcm.liste_questions) == 0:
                messagebox.showwarning(
                    title="Questionnaire incomplet",
                    message="Veuillez renseigner au moins 1 question.",
                )

                return False

            for i, question in enumerate(self.qcm.liste_questions):
                if not question.coherent():
                    logger.info(f"Question #{i} is incoherent: {question}")

                    messagebox.showwarning(
                        title="Questionnaire incomplet",
                        message=f"Veuillez renseigner des réponses à toutes les"
                        f" questions avant de valider (réponse incohérente"
                        f" à la question {i + 1})",
                    )

                    return False

            self.tentative = Tentative(qcm=self.qcm)
            self.states[AppState.ANSWER].set_tentative(self.tentative)
            self.appstate = AppState.ANSWER
            return True

        else:
            return False

    def verifier_tentative(self) -> None:
        score = 0
        score_max = 0

        for i, each_reponse in enumerate(self.tentative.liste_reponses):
            if not each_reponse.has_answer():
                logger.info(f"Reponse #{i} has no answer: {each_reponse}")

                messagebox.showwarning(
                    title="Formulaire incomplet",
                    message=f"Veuillez répondre à toutes les questions avant"
                    f" de valider (pas de réponse à la question {i + 1})",
                )

                return

            score_max += each_reponse.question.points
            score += each_reponse.points

            logger.debug(f"Reponse #{i} has score {each_reponse.points}")

        self.states[AppState.CORRECTION].set_tentative(self.tentative)
        self.appstate = AppState.CORRECTION
        logger.debug(f"Tentative score is {score} / {score_max}")

        messagebox.showinfo(
            title="Score",
            message=f"Votre score est de {score} sur {score_max}.",
        )

    def save_tentative(self) -> None:
        raise NotImplementedError

    def save_tentative_as(self) -> None:
        raise NotImplementedError

    def close_tentative(self) -> None:
        raise NotImplementedError

    def editer_qcm(self) -> None:
        self.qcm = self.tentative.qcm
        # TODO: enregistrer la Tentative ?
        self.tentative = None
        self.states[AppState.EDIT].set_qcm(self.qcm)
        self.appstate = AppState.EDIT
