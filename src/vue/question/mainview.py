import logging

from ttkbootstrap import Button, Entry, Frame, StringVar
from ttkbootstrap.scrolled import ScrolledFrame

from model.qcm import Qcm
from model.question import (
    Question,
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)

from .callback_type import CallbackCommand
from .ui import QuestionLibreUI, QuestionQCMultiplesUI, QuestionQCUniqueUI, QuestionUI


class MainView(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=800)
        self.pack_propagate(False)

        self.titre_var = StringVar()
        self.titre = Entry(self, textvariable=self.titre_var)
        self.titre.pack(pady=10)

        self.questions_ui = []

        self.scroll_outer = ScrolledFrame(self, autohide=True)
        self.scroll_outer.pack(fill="both", expand=True, padx=20, pady=20)
        self.scroll_container = Frame(self.scroll_outer)
        self.scroll_container.pack(fill="both", expand=True, padx=(0, 10))

        self.btn_ajouter = Button(
            self.scroll_container,
            text="➕ Ajouter une nouvelle question",
            command=self.ajouter_question,
            style="info",
        )

    def _editeur_callback(self, command: CallbackCommand, question_ui: QuestionUI):
        try:
            question_index = self.questions_ui.index(question_ui)
        except ValueError:
            raise ValueError("Question not found in the list")

        match command:
            case CallbackCommand.DELETE:
                self.qcm.liste_questions.pop(question_index)

            case CallbackCommand.CHANGE_TYPE:
                match question_ui.type_var.get():
                    case QuestionLibreUI.question_type:
                        question_class = QuestionLibre

                    case QuestionQCMultiplesUI.question_type:
                        question_class = QuestionQCMultiples

                    case QuestionQCUniqueUI.question_type:
                        question_class = QuestionQCUnique

                    case _:
                        raise ValueError(
                            f"Unknown question type '{question_ui.type_var.get()}'"
                        )

                question = question_class(
                    question_ui.question.enonce, question_ui.question.points
                )

                self.__open_question(question)
                self.qcm.liste_questions[question_index] = question

            case CallbackCommand.DUPLICATE:
                raise NotImplementedError

            case CallbackCommand.MOVE_UP:
                if question_index > 0:
                    self.qcm.liste_questions.insert(
                        question_index - 1, self.qcm.liste_questions.pop(question_index)
                    )

            case CallbackCommand.MOVE_DOWN:
                if question_index + 1 < len(self.qcm.liste_questions):
                    self.qcm.liste_questions.insert(
                        question_index + 1, self.qcm.liste_questions.pop(question_index)
                    )

        self.update_view()

    def update_view(self):
        self.titre_var.set(self.qcm.titre)

        for question_ui in self.questions_ui:
            question_ui.pack_forget()
        self.btn_ajouter.pack_forget()

        self.questions_ui = []
        for question in self.qcm.liste_questions:
            self.__open_question(question)
        self.btn_ajouter.pack(pady=20)

    def ajouter_question(self):
        question = QuestionQCUnique("Nouvelle question", 1)

        self.__open_question(question)
        self.qcm.liste_questions.append(question)
        self.update_view()

        logging.info("Nouvelle question ajoutée")

    def __open_question(self, question: Question):
        ui_class = None

        match question:
            case QuestionQCUnique():
                ui_class = QuestionQCUniqueUI

            case QuestionQCMultiples():
                ui_class = QuestionQCMultiplesUI

            case QuestionLibre():
                ui_class = QuestionLibreUI

            case _:
                raise ValueError(
                    f"Unsupported question type of class "
                    f"'{question.__class__.__name__}'"
                )

        question_ui = ui_class(
            self.scroll_container,
            page_callback=self._editeur_callback,
            question=question,
        )
        question_ui.pack(fill="x", pady=10)
        self.questions_ui.append(question_ui)

    def set_qcm_new(self):
        self.set_qcm(Qcm("Nouveau questionnaire"))
        self.ajouter_question()

    def set_qcm(self, qcm: Qcm):
        logging.info(f"Opening qcm '{qcm.titre}'")
        self.qcm = qcm

        for i, question in enumerate(qcm.liste_questions):
            try:
                self.__open_question(question)
            except ValueError as e:
                logging.error(f"Failed to open question #{i}: {e.message}")

        self.update_view()
