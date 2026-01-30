import pytest
from model.question import QuestionQCUnique, QuestionQCMultiples, QuestionLibre
from model.reponse import ReponseQCUnique, ReponseQCMultiples, ReponseLibre
from model.qcm import Qcm


def test_qcm_unique_verification():
    """Vérifie qu'un QCM unique valide uniquement le bon index."""
    q = QuestionQCUnique(
        enonce="Capitale ?", points=1, choix_rep=["Paris", "Lyon"], id_bonne_reponse=0
    )
    verif = ReponseQCUnique(q)

    assert verif.verifier(0) is True, "0 est l'index de la bonne réponse"
    assert verif.verifier(1) is False, "1 est une mauvaise réponse"


def test_qcm_multiple_verification():
    """Vérifie la logique pour les QCM à réponses multiples."""
    q = QuestionQCMultiples(
        enonce="Fruits rouges ?",
        points=1,
        choix_rep=["Fraise", "Banane", "Cerise"],
        index_bonne_reponse=[0, 2],  # Fraise et Cerise
    )
    verif = ReponseQCMultiples(q)
    assert verif.verifier(0) is True
    assert verif.verifier(2) is True
    assert verif.verifier(1) is False


def test_question_libre_verification():
    """Vérifie la robustesse (majuscules/espaces) de la question libre."""
    q = QuestionLibre(enonce="Planète rouge ?", points=2, rep_attendue="Mars")
    verif = ReponseLibre(q)

    assert verif.verifier("Mars") is True
    assert verif.verifier("mars") is True
    assert verif.verifier("  MARS  ") is True
    assert verif.verifier("Jupiter") is False


@pytest.fixture
def qcm_vide():
    """
    Fixture : Prépare un objet Qcm neuf pour chaque test qui en a besoin.
    Évite de répéter la création dans chaque fonction (DRY).
    """
    return Qcm("Test Général")


def test_ajout_question(qcm_vide):
    """On injecte la fixture 'qcm_vide' en argument."""
    q1 = QuestionLibre("Q1", 1, "R")

    qcm_vide.ajouter_question(q1)

    assert qcm_vide.get_nombre_questions() == 1
    assert qcm_vide.get_question(0) == q1


def test_calcul_score_max(qcm_vide):
    """Vérifie que le modèle calcule bien la somme des points."""
    q1 = QuestionQCUnique("Q1", 2, [], 0)  # 2 points
    q2 = QuestionLibre("Q2", 3, "R")  # 3 points

    qcm_vide.ajouter_question(q1)
    qcm_vide.ajouter_question(q2)

    assert qcm_vide.calculer_score_max() == 5


def test_suppression_question(qcm_vide):
    q1 = QuestionLibre("Q1", 1, "R")
    qcm_vide.ajouter_question(q1)

    qcm_vide.supprimer_question(0)

    assert qcm_vide.get_nombre_questions() == 0
