#!/usr/bin/env python
from ttkbootstrap import Window, Button
from ttkbootstrap.scrolled import ScrolledFrame
from vue.editeur.choix_unique import ChoixUnique

class Main:
    def __init__(self):
        self.window = Window(themename="flatly")
        self.window.title("QCM LPORM")
        self.window.geometry("900x700")

        self.questions_creees = []

        # 1. On place le bouton en HAUT pour qu'il reste visible
        self.btn_ajouter = Button(
            self.window, 
            text="➕ Ajouter une nouvelle question", 
            command=self.ajouter_question,
            style="info"
        )
        self.btn_ajouter.pack(pady=10)

        # 2. Le conteneur avec défilement prend tout le reste de la place
        self.scroll_container = ScrolledFrame(self.window, autohide=True)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Lancement automatique de la première question
        self.ajouter_question()

    def ajouter_question(self):
        # CORRECTION : On utilise self.scroll_container au lieu de self.main_frame
        nouvelle_qst = ChoixUnique(self.scroll_container)
        nouvelle_qst.pack(fill="x", pady=10)
        
        self.questions_creees.append(nouvelle_qst)

    def main(self):
        self.window.mainloop()

if __name__ == "__main__":
    Main().main()