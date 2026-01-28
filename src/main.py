#!/usr/bin/env python

from ttkbootstrap import Window

from vue.editeur.choix_unique import ChoixUnique

class Main:
    def __init__(self):
        self.window = Window()

        ChoixUnique(self.window, choix=["a", "b", "c"]).pack()

    def main(self):
        self.window.mainloop()

if __name__ == "__main__":
    Main().main()
