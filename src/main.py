#!/usr/bin/env python
from ttkbootstrap import Window

from vue.editeur.editeur_page import EditeurPage
from vue.reponse.reponse_page import ReponsePage

from model.qcm import Qcm
from model.question import QuestionQCUnique, QuestionQCMultiples, QuestionLibre

import logging
logging.basicConfig(level=logging.DEBUG)


class Main:
    def __init__(self):
        self.window = Window(themename="flatly")
        self.window.title("QCM LPORM")
        self.window.geometry("900x700")

        qcm = Qcm(titre="QCM de test")
        qcm.ajouter_question(
            QuestionQCUnique(
                enonce="Ceci est un test",
                points=3,
                choix_rep=["hello", "world"],
                id_bonne_reponse=0
            )
        )
        qcm.ajouter_question(
            QuestionQCMultiples(
                enonce="Ceci est un test",
                points=3,
                choix_rep=["hello", "world", "Faux"],
                id_bonne_reponse=[0, 1]
            )
        )
        qcm.ajouter_question(
            QuestionLibre(
                enonce="Ceci est un test",
                points=1,
                rep_attendue="bien"
            )
        )

        # EditeurPage(self.window).pack(fill="y", expand=True)
        ReponsePage(self.window, qcm).pack(fill="y", expand=True)

    def main(self):
        self.window.mainloop()


if __name__ == "__main__":
    Main().main()
