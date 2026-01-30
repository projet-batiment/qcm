from ttkbootstrap import Frame, Button, Entry, StringVar
from ttkbootstrap.scrolled import ScrolledFrame
import logging
from vue.editeur.editeur_callback_type import CallbackCommand
from vue.editeur.choix_unique import ChoixUnique
from vue.editeur.choix_multiple import ChoixMultiple 
from vue.editeur.editeur import Editeur

class EditeurPage(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=800)
        self.pack_propagate(False)

        self.titre_var = StringVar(value="Titre du questionnaire")
        self.titre = Entry(self, textvariable=self.titre_var)
        self.titre.pack(pady=10)

        self.questions = []
        self.scroll_outer = ScrolledFrame(self, autohide=True)
        self.scroll_outer.pack(fill="both", expand=True, padx=20, pady=20)
        self.scroll_container = Frame(self.scroll_outer)
        self.scroll_container.pack(fill="both", expand=True, padx=(0, 10))

        self.btn_ajouter = Button(
            self.scroll_container,
            text="➕ Ajouter une nouvelle question",
            command=self.ajouter_question,
            style="info"
        )

        self.ajouter_question()

    def _editeur_callback(self, command: CallbackCommand, question: Editeur):
        try:
            question_index = self.questions.index(question)
        except ValueError as e:
            logging.error("question not found in the list")
            raise e

        match command:
            case CallbackCommand.DELETE:
                question.destroy()
                self.questions.pop(question_index)

            case CallbackCommand.CHANGE_TYPE:
              
                nouveau_type = question.type_var.get()
                donnees = {
                    "titre": question.titre_var.get(),
                    "points": question.points_var.get(),
                    "obligatoire": question.obligatoire_var.get(),
                    "choix": getattr(question, 'choix', None)
                }

                
                question.destroy()

              
                if nouveau_type == "Choix Multiple":
                    nouvelle_q = ChoixMultiple(self.scroll_container, page_callback=self._editeur_callback, **donnees)
                else:
                    nouvelle_q = ChoixUnique(self.scroll_container, page_callback=self._editeur_callback, **donnees)
                
           
                nouvelle_q.type_var.set(nouveau_type)

          
                self.questions[question_index] = nouvelle_q

            case CallbackCommand.DUPLICATE:
                raise NotImplementedError

            case CallbackCommand.MOVE_UP:
                if (question_index > 0):
                    self.questions.insert(question_index-1, self.questions.pop(question_index))

            case CallbackCommand.MOVE_DOWN:
                if (question_index+1 < len(self.questions)):
                    self.questions.insert(question_index+1, self.questions.pop(question_index))

        self.update_questions_view()

    def update_questions_view(self):

        for each in self.questions:
            each.pack_forget()
        
        self.btn_ajouter.pack_forget()

        for each in self.questions:
            each.pack(fill="x", pady=10)

        self.btn_ajouter.pack(pady=20)

    def ajouter_question(self):
        self.questions.append(ChoixUnique(
            self.scroll_container,
            page_callback=self._editeur_callback,
        ))
        self.update_questions_view()