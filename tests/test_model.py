import model.qcm  # noqa: F401
import pytest
from model.question import QuestionQCMultiples, QuestionQCUnique
from model.reponse import ReponseQCMultiples, ReponseQCUnique

# noqa: F401 : Afin que Ruff ne se plaigne pas de l'import non utilisé.


def test_qcm_unique_verification():
    """Vérifie qu'un QCM unique valide uniquement le bon index."""
    q = QuestionQCUnique(
        enonce="Capitale ?",
        points=1,
        choix_rep=["Paris", "Lyon"],
        id_bonne_reponse=0,
        obligatoire=True,
    )
    verif = ReponseQCUnique(q)

    assert verif.verifier(0) is True
    assert verif.verifier(1) is False


@pytest.mark.parametrize(
    "choix_utilisateur, resultat_attendu",
    [
        (0, True),
        (2, True),
        (1, False),
    ],
)
def test_qcm_multiple_verification(choix_utilisateur, resultat_attendu):
    """Vérifie la logique pour les QCM à réponses multiples."""
    q = QuestionQCMultiples(
        enonce="Fruits rouges ?",
        points=1,
        choix_rep=["Fraise", "Banane", "Cerise"],
        id_bonne_reponse=[0, 2],  # Fraise et Cerise
        obligatoire=True,
    )
    verif = ReponseQCMultiples(q)

    assert verif.verifier(choix_utilisateur) is resultat_attendu
