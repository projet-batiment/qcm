#!/usr/bin/env python
from ttkbootstrap import Window
from vue.editeur.editeur_page import EditeurPage

class Main:
    def __init__(self):
        self.window = Window(themename="flatly")
        self.window.title("QCM LPORM")
        self.window.geometry("900x700")

        EditeurPage(self.window).pack(fill="y", expand=True)

    def main(self):
        self.window.mainloop()


if __name__ == "__main__":
    Main().main()
