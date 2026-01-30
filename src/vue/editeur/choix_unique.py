from ttkbootstrap import Frame, Entry, Radiobutton, IntVar, Button, StringVar
from tkinter import LEFT, TOP, RIGHT, BOTTOM

from .editeur import Editeur

class ChoixUnique(Editeur):
    def __init__(self, parent, choix=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.container = Frame(self.milieu)
        self.container.pack(fill="x", expand=True)
        if choix is None:
            self.choix = ["Option 1", "Option 2", "Option 3"]
        else:
            self.choix = choix
        self.choix_ui = []
        self.choix_var = IntVar(value=-1)
        self.vars = []

        def add():
            self.choix.append("Nouveau choix")
            self.update()
        add_button = Button(self.container, text="Ajouter", command=add)
        add_button.pack(side=BOTTOM)

        self.update()

    def update(self):
        for each_old_ui in self.choix_ui:
            each_old_ui.pack_forget()

        self.choix_ui = []
        self.vars = []

        for i, each_choix in enumerate(self.choix):
            each_frame = Frame(self.container)
            each_frame.pack(side=TOP, fill="x", expand=True)

            each_var = StringVar(value=each_choix)
            self.vars.append(each_var)
            each_radio = Radiobutton(each_frame, value=i, variable=self.choix_var)
            each_radio.pack(side=LEFT)
            each_entry = Entry(each_frame, textvariable=each_var)
            each_entry.pack(side=LEFT)

            def delete(i=i):
                self.choix.pop(i)
                self.update()
            each_delete = Button(each_frame, text=" ⤫ ", command=delete, style="warning")
            each_delete.pack(side=RIGHT)

            def move_down(i=i):
                self.choix.insert(i+1, self.choix.pop(i))
                self.update()
            each_move_down = Button(each_frame, text=" 🠋 ", command=move_down)
            each_move_down.pack(side=RIGHT)
            if i+1 == len(self.choix):
                each_move_down.config(state="disabled")

            def move_up(i=i):
                self.choix.insert(i-1, self.choix.pop(i))
                self.update()
            each_move_up = Button(each_frame, text=" 🠉 ", command=move_up)
            each_move_up.pack(side=RIGHT)
            if i == 0:
                each_move_up.config(state="disabled")

            self.choix_ui.append(each_frame)
