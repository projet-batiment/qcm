import os

import pytest
from sqlalchemy import text

from qcm.control.bdd_manager import BddManager
from qcm.model.qcm import Qcm
from qcm.model.question import QuestionLibre, QuestionQCMultiples, QuestionQCUnique


# "fixture" prépare une bdd vide avant chaque test et la nettoie après
@pytest.fixture
def bdd_test():
    if os.path.exists("test_qcm.db"):
        try:
            os.remove("test_qcm.db")
        except PermissionError:
            pass
    manager = BddManager("test_qcm.db")
    yield manager

    manager.close_bdd()

    if os.path.exists("test_qcm.db"):
        try:
            os.remove("test_qcm.db")
        except PermissionError:
            print("Attention: Impossible de supprimer test_qcm.db immédiatement.")


def test_sauvegarde_relecture(bdd_test):
    q = QuestionLibre("Test ?", 1, "Oui")
    qcm = Qcm("Test", [q])
    bdd_test.save_qcm(qcm)
    liste = bdd_test.get_qcms()
    assert len(liste) == 1
    assert liste[0].titre == "Test"
    assert liste[0].liste_questions[0].rep_attendue == "Oui"


def test_scenario_complet_creation_lecture(bdd_test):
    """
    Test inspiré de ce qui avait été fait dans le bdd_manager.py:
    Crée un QCM mixte (Multiple + Libre), sauvegarde et vérifie TOUT en détail.
    """
    q_multi = QuestionQCMultiples(
        enonce="Quels sont les chiffres pairs ?",
        points=2,
        choix_rep=["1", "2", "3", "4"],
        id_bonne_reponse={1, 3},  # Index 1 ('2') et 3 ('4')
    )

    q_libre = QuestionLibre(
        enonce="Capitale de la France ?", points=1, rep_attendue="Paris"
    )

    mon_qcm = Qcm("Test Complet", [q_multi, q_libre])
    assert bdd_test.save_qcm(mon_qcm) is True

    bdd_test.session.expire_all()
    qcms_relecture = bdd_test.get_qcms()

    assert len(qcms_relecture) == 1
    qcm = qcms_relecture[0]

    assert qcm.titre == "Test Complet"
    assert len(qcm.liste_questions) == 2

    q1 = qcm.liste_questions[0]
    assert isinstance(q1, QuestionQCMultiples)
    assert q1.enonce == "Quels sont les chiffres pairs ?"
    assert q1.points == 2
    assert len(q1.choix_rep) == 4
    assert q1.choix_rep[0] == "1"
    assert q1.choix_rep[1] == "2"
    assert q1.id_bonne_reponse == {1, 3}

    q2 = qcm.liste_questions[1]
    assert isinstance(q2, QuestionLibre)
    assert q2.enonce == "Capitale de la France ?"
    assert q2.rep_attendue == "Paris"


def test_modification_qcm(bdd_test):
    """Vérifie qu'on peut modifier un QCM existant (Update)"""

    q = QuestionQCUnique("Il fait chaud ?", 1, ["Oui", "Non"], 0)
    qcm = Qcm("QCM Modifiable", [q])
    bdd_test.save_qcm(qcm)
    qcm_a_modif = bdd_test.get_qcms()[0]
    qcm_a_modif.titre = "Titre Modifié"

    q_modif = qcm_a_modif.liste_questions[0]
    q_modif.enonce = "Vraiment Chaud ?"  # On change énoncé etc..
    q_modif.points = 5
    q_modif.choix_rep = ["Vrai", "Faux"]
    q_modif.id_bonne_reponse = 1  # On change la bonne réponse pour 'Faux'

    bdd_test.session.commit()

    bdd_test.session.expire_all()
    qcm_relu = bdd_test.get_qcms()[0]

    assert qcm_relu.titre == "Titre Modifié"
    assert qcm_relu.liste_questions[0].enonce == "Vraiment Chaud ?"
    assert qcm_relu.liste_questions[0].points == 5
    assert qcm_relu.liste_questions[0].choix_rep == ["Vrai", "Faux"]
    assert qcm_relu.liste_questions[0].id_bonne_reponse == 1


def test_suppression_cascade(bdd_test):
    """
    Vérifie que si on supprime un QCM, ses questions et ses choix
    sont aussi supprimés de la BDD (nettoyage propre).
    """
    q = QuestionQCMultiples("Test", 1, ["A", "B"], [0])
    qcm = Qcm("A Supprimer", [q])
    bdd_test.save_qcm(qcm)

    # On récupère les ID pour vérifier après suppression
    qcm_id = qcm.id
    question_id = q.id
    choix_id = q.choix_bdd[0].id

    bdd_test.delete_qcm(qcm)
    assert bdd_test.session.get(Qcm, qcm_id) is None  # QCM bien supprimé ?

    # Les Questions (Doivent être supprimées : None)
    res_q = bdd_test.session.execute(
        text(f"SELECT * FROM questions WHERE id={question_id}")
    ).fetchone()
    assert res_q is None

    # Les choix/réponses Doivent être supprimées : None)
    res_c = bdd_test.session.execute(
        text(f"SELECT * FROM choix WHERE id={choix_id}")
    ).fetchone()
    assert res_c is None
