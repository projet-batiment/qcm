from logging import getLogger

from sqlalchemy.orm import Session

from qcm.db.qcm import Base, QcmDB
from qcm.db.question import (
    QuestionLibreDB,
    QuestionQCMultiplesDB,
    QuestionQCUniqueDB,
)
from qcm.db.tentative import TentativeDB
from qcm.db.reponse import (
    ReponseDB,
    ReponseLibreDB,
    ReponseQCMultiplesDB,
    ReponseQCUniqueDB,
)

from qcm.model.qcm import Qcm
from qcm.model.question import (
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)
from qcm.model.tentative import Tentative
from qcm.model.reponse import (
    ReponseLibre,
    ReponseQCMultiples,
    ReponseQCUnique,
)

logger = getLogger(__name__)

def convert_qcm(session: Session, qcm: Qcm) -> QcmDB:
    logger.debug("Creating qcm object")
    db_qcm = QcmDB(qcm.titre)
    session.add(db_qcm)
    session.flush()

    logger.debug("Populating qcm object")
    for question in qcm.liste_questions:
        arguments = {
            "enonce": question.enonce,
            "points": question.points,
            "obligatoire": question.obligatoire,
        }

        logger.debug(f"Creating question {question.__class__.__name__} object")
        match question:
            case QuestionQCUnique():
                db_question = QuestionQCUniqueDB(**arguments)
                session.add(db_question)
                session.flush()

                db_question.choix_rep = question.choix
                db_question.id_bonne_reponse = question.index_bonne_reponse
                session.flush()

            case QuestionQCMultiples():
                db_question = QuestionQCMultiplesDB(**arguments)
                session.add(db_question)
                session.flush()

                db_question.choix_rep = question.choix
                db_question.id_bonne_reponse = question.index_bonnes_reponses
                session.flush()

            case QuestionLibre():
                db_question = QuestionLibreDB(
                    rep_attendue=question.rep_attendue,
                    **arguments,
                )
                session.add(db_question)
                session.flush()

            case _:
                raise ValueError(
                    f"Unkown model question type"
                    f" {question.__class__.__name__}"
                )

        db_qcm.liste_questions.append(db_question)

        if hasattr(db_question, "choix_bdd"):
            for each in db_question.choix_bdd:
                session.add(each)

        # save the operations in memory without commiting to file
        session.flush()

    return db_qcm

def convert_tentative(session: Session, tentative: Tentative, expected_db_qcm: QcmDB) -> TentativeDB:
    logger.debug("Creating tentative object")
    db_tentative = TentativeDB(tentative.nom)
    session.add(db_tentative)

    logger.debug("Populating tentative object")

    # NOTE: all tentatives should have the same qcm
    #       it is then constructed only once
    #       and conditions are ensured in higher level (db_manager)
    db_tentative.qcm = expected_db_qcm
    session.flush()

    for i, reponse in enumerate(tentative.liste_reponses):
        arguments = {
            "question": expected_db_qcm.liste_questions[i],
            "tentative": db_tentative,
        }

        logger.debug(f"Creating reponse {reponse.__class__.__name__} object")
        match reponse:
            case ReponseQCUnique():
                db_reponse = ReponseQCUniqueDB(
                    choix=reponse.reponse_choisie,
                    **arguments,
                )
                session.add(db_reponse)
                session.flush()

            case ReponseQCMultiples():
                db_reponse = ReponseQCMultiplesDB(
                    choix=reponse.reponses_choisies,
                    **arguments,
                )
                session.add(db_reponse)
                session.flush()

            case ReponseLibre():
                db_reponse = ReponseLibreDB(
                    reponse=reponse.reponse,
                    **arguments,
                )
                session.add(db_reponse)
                session.flush()

            case _:
                raise ValueError(
                    f"Unkown model question type"
                    f" {reponse.__class__.__name__}"
                )

        db_tentative.liste_reponses.append(db_reponse)

        if hasattr(db_reponse, "choix_bdd"):
            for each in db_reponse.choix_bdd:
                session.add(each)

        # save the operations in memory without commiting to file
        session.flush()

    return db_tentative
