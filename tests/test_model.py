import model.qcm  # noqa: F401
from model.question import QuestionQCMultiples, QuestionQCUnique
from model.reponse import ReponseQCMultiples, ReponseQCUnique

# noqa: F401 : Afin que Ruff ne se plaigne pas de l'import non utilisé.


def test_qcm_unique_verification():
    """Vérifie qu'un QCM unique valide uniquement le bon index."""
    q = QuestionQCUnique(
        enonce="Capitale ?", points=1, choix_rep=["Paris", "Lyon"], id_bonne_reponse=0
    )
    verif = ReponseQCUnique(q)

    assert verif.verifier(0) is True
    assert verif.verifier(1) is False


def test_qcm_multiple_verification():
    """Vérifie la logique pour les QCM à réponses multiples."""
    q = QuestionQCMultiples(
        enonce="Fruits rouges ?",
        points=1,
        choix_rep=["Fraise", "Banane", "Cerise"],
        id_bonne_reponse=[0, 2],  # Fraise et Cerise
    )
    verif = ReponseQCMultiples(q)

    assert verif.verifier(0) is True
    assert verif.verifier(2) is True
    assert verif.verifier(1) is False
