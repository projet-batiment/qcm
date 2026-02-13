import pytest

import qcm.model.qcm  # noqa: F401
from qcm.model.question import QuestionQCMultiples, QuestionQCUnique
from qcm.model.reponse import ReponseQCMultiples, ReponseQCUnique

# noqa: F401 : Afin que Ruff ne se plaigne pas de l'import non utilisé.


@pytest.mark.parametrize(
    "choix_utilisateur, resultat_attendu",
    [
        (0, True),
        (1, False),
    ],
)
def test_qcm_unique_verification(choix_utilisateur, resultat_attendu):
    """Vérifie qu'un QCM unique valide uniquement le bon index."""
    reponse = ReponseQCUnique(
        question=QuestionQCUnique(
            choix=["Paris", "Lyon"],
            index_bonne_reponse=0,
        ),
        reponse_choisie=choix_utilisateur,
    )

    assert reponse.verifier() is resultat_attendu


@pytest.mark.parametrize(
    "choix_utilisateur, resultat_attendu",
    [
        ([0, 2], True),
        ([0], False),
        ([0, 1], False),
    ],
)
def test_qcm_multiple_verification(choix_utilisateur, resultat_attendu):
    reponse = ReponseQCMultiples(
        question=QuestionQCMultiples(
            choix=["Fraise", "Banane", "Cerise"],
            index_bonnes_reponses=[0, 2],  # Fraise et Cerise
        ),
        reponses_choisies=choix_utilisateur,
    )

    assert reponse.verifier() is resultat_attendu
