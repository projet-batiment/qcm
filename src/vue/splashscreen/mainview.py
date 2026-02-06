from ttkbootstrap import Frame, Label

class MainView(Frame):
    def __init__(self, controller):
        super().__init__()

        container = Frame(self)
        container.pack(expand=True)

        title = Label(container, text="Bienvenue !")
        title.pack()

        instruction = Label(container, text="Utilisez le menu pour ouvrir un créer un questionnaire.")
        instruction.pack()
