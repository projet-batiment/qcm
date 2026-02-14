from logging import getLogger

from qcm.db.qcm import QcmDB
from qcm.db.question import (
    QuestionLibreDB,
    QuestionQCMultiplesDB,
    QuestionQCUniqueDB,
)
from qcm.db.reponse import (
    ReponseLibreDB,
    ReponseQCMultiplesDB,
    ReponseQCUniqueDB,
)
from qcm.db.tentative import TentativeDB
from qcm.model.qcm import Qcm
from qcm.model.question import (
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)
from qcm.model.tentative import Tentative

logger = getLogger(__name__)


def convert_qcm(db_qcm: QcmDB) -> Qcm:
    qcm = Qcm(titre=db_qcm.titre)

    for db_question in db_qcm.liste_questions:
        arguments = {
            "enonce": db_question.enonce,
            "points": db_question.points,
            "obligatoire": db_question.obligatoire,
        }

        match db_question:
            case QuestionQCUniqueDB():
                question = QuestionQCUnique(
                    choix=db_question.choix_rep,
                    index_bonne_reponse=db_question.id_bonne_reponse,
                    **arguments,
                )

            case QuestionQCMultiplesDB():
                question = QuestionQCMultiples(
                    choix=db_question.choix_rep,
                    index_bonnes_reponses=db_question.id_bonne_reponse,
                    **arguments,
                )

            case QuestionLibreDB():
                question = QuestionLibre(
                    rep_attendue=db_question.rep_attendue,
                    **arguments,
                )

            case _:
                raise ValueError(
                    f"Unkown db question type{db_question.__class__.__name__}"
                )

        qcm.liste_questions.append(question)

    return qcm


def convert_tentative(db_tentative: TentativeDB, expected_qcm: Qcm) -> Tentative:
    # NOTE: all tentatives should have the same qcm
    #       it is then constructed only once
    #       and conditions are ensured in higher level (db_manager)
    tentative = Tentative(qcm=expected_qcm, nom=db_tentative.nom)

    for i, db_reponse in enumerate(db_tentative.liste_reponses):
        reponse = tentative.liste_reponses[i]
        match db_reponse:
            case ReponseQCUniqueDB():
                reponse.reponse_choisie = db_reponse.get_choix()

            case ReponseQCMultiplesDB():
                reponse.reponses_choisies = set(db_reponse.choix)

            case ReponseLibreDB():
                reponse.reponse = db_reponse.reponse

            case _:
                raise ValueError(
                    f"Unkown db reponse type{db_reponse.__class__.__name__}"
                )

        # initializing Tentative already creates and populates liste_reponses:
        # no need for tentative.liste_reponses.append(reponse)

    return tentative
