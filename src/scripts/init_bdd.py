import os

from control.bdd_manager import BddManager
from model.qcm import Qcm
from model.question import QuestionQCMultiples, QuestionLibre


def init_db():
    print("Suppression de l'ancienne base de données...")
    if os.path.exists("qcm.db"):
        os.remove("qcm.db")

    bdd = BddManager()

    print("Ajout une question de démo")
    q1 = QuestionQCMultiples("2+2 ?", 1, ["3", "4", "5"], [1])
    q2 = QuestionLibre("Les Goats ?", 2, "LPorm")

    qcm = Qcm("QCM", [q1, q2])
    bdd.save_qcm(qcm)

    print("BDD réinitialisée avec succès.")
    bdd.close_bdd()


if __name__ == "__main__":
    init_db()
