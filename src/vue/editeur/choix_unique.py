from ttkbootstrap import Frame, Entry

class ChoixUnique(Frame):
    def __init__(self, titre="", choix=None, obligatoire=True):
        super().__init__()
        
        self.titre = titre
        self.choix = [] if choix is None else choix
        self.obligatoire = obligatoire

        self.haut = Frame(self)
        self.haut.pack()

        self.titre_entry = Entry("Titre par défaut")
        self.titre_entry.pack()

        self.milieu = Frame(self)
        self.milieu.pack()

        self.bas = Frame(self)
        self.bas.pack()