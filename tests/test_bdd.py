from tempfile import NamedTemporaryFile

from dataclasses import dataclass, field

import pytest

from qcm.control.db_manager import read_from_file, save_to_file
from qcm.model.qcm import Qcm
from qcm.model.tentative import Tentative
from qcm.model.data import QcmData
from qcm.model.question import QuestionLibre, QuestionQCMultiples, QuestionQCUnique
from qcm.model.reponse import ReponseLibre, ReponseQCMultiples, ReponseQCUnique


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


@pytest.fixture
def data() -> QcmData:
    qcm = Qcm(
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

    tentatives: list[Tentative] = []

    erronee = Tentative(qcm)
    erronee.liste_reponses[0].reponse_choisie = 1
    erronee.liste_reponses[1].reponses_choisies = {2}
    erronee.liste_reponses[2].reponses_choisies = "faux"
    tentatives.append(erronee)

    juste = Tentative(qcm)
    juste.liste_reponses[0].reponse_choisie = qcm.liste_questions[0].index_bonne_reponse
    juste.liste_reponses[1].reponses_choisies = qcm.liste_questions[1].index_bonnes_reponses
    juste.liste_reponses[2].reponses_choisies = qcm.liste_questions[2].rep_attendue
    tentatives.append(juste)

    moyen = Tentative(qcm)
    moyen.liste_reponses[0].reponse_choisie = erronee.liste_reponses[0].reponse_choisie
    moyen.liste_reponses[1].reponses_choisies = qcm.liste_questions[1].index_bonnes_reponses
    moyen.liste_reponses[2].reponses_choisies = qcm.liste_questions[2].rep_attendue
    tentatives.append(moyen)

    return QcmData(
        qcm,
        tentatives,
    )


def test_sauvegarde_puis_relecture(data: QcmData):
    with NamedTemporaryFile(delete=True) as file:
        save_to_file(data, file.name)
        read_data = read_from_file(file.name)

        assert read_data == data
