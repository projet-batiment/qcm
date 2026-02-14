from ttkbootstrap import Frame, Label

from qcm.vue.parent import Parent


class MainView(Frame):
    """
    Conteneur premier niveau pour le mode Page d'Accueil.
    N'est instanciée qu'une seule fois par exécution.
    """

    def __init__(self, parent: Parent):
        """
        Args:
            parent (Parent): the parent container
        """

        super().__init__(parent)

        container = Frame(self)
        container.pack(expand=True)

        title = Label(container, text="Bienvenue !")
        title.pack()

        instruction = Label(
            container, text="Utilisez le menu pour ouvrir un créer un questionnaire."
        )
        instruction.pack()
