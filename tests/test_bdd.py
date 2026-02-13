from tempfile import NamedTemporaryFile

import pytest

from qcm.control.db_manager import read_from_file, save_to_file
from qcm.model.qcm import Qcm
from qcm.model.question import QuestionLibre, QuestionQCMultiples, QuestionQCUnique


@pytest.fixture
def qcm_test():
    return Qcm(
        titre="QCM de test",
        liste_questions=[
            QuestionQCUnique(
                enonce="Test de choix unique",
                points=3,
                choix=["hello", "world", "!"],
                index_bonne_reponse=0,
            ),
            QuestionQCMultiples(
                enonce="Test de choix multiples",
                points=2,
                choix=["hello", "world", "!"],
                index_bonnes_reponses={0, 1},
            ),
            QuestionLibre(
                enonce="Test de texte libre",
                points=1,
                rep_attendue="bien",
            ),
        ],
    )


def test_sauvegarde_puis_relecture(qcm_test):
    with NamedTemporaryFile(delete=True) as file:
        save_to_file(qcm_test, file.name)
        read_qcm = read_from_file(file.name)

        assert read_qcm == qcm_test
