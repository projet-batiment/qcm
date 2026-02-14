from contextlib import contextmanager
from logging import getLogger
from typing import ContextManager

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from qcm.db.qcm import Base, QcmDB
from qcm.db.question import (
    QuestionLibreDB,
    QuestionQCMultiplesDB,
    QuestionQCUniqueDB,
)
from qcm.model.qcm import Qcm
from qcm.model.question import (
    QuestionLibre,
    QuestionQCMultiples,
    QuestionQCUnique,
)

logger = getLogger(__name__)


@contextmanager
def open_session(filename: str) -> ContextManager[Session]:
    """
    Ouvre un fichier et crée un engine et une session sqlalchemy.
    Finit par fermer la connection.

    Args:
        filename (str): chemin du fichier à ouvrir

    Yields:
        Session: la session ouverte

    Raises:
        SQLAlchemyError
        Exception (transmission d'exceptions non gérées)
    """

    logger.debug(f"Ouverture du fichier '{filename}'")

    extention = filename.split(".")[-1]
    if not extention == "dbq":
        logger.warning(f"Expected .dbq extention, found '{extention}'")

    engine = create_engine(
        f"sqlite:///{filename}",
        connect_args={"check_same_thread": False},
        echo=False,
    )

    # database structure
    if not inspect(engine).get_table_names():
        try:
            logger.debug("Aucune table trouvée: Initialisation de la base de donnée")
            Base.metadata.create_all(engine)
            logger.info("Base de données initialisée.")
        except SQLAlchemyError as e:
            logger.critical(f"Impossible de créer les tables : {e}")
            raise e
    else:
        logger.debug("La base de données contient déjà une structure de données")

    # handle ourself session and engine disposal
    try:
        logger.info("Session de la bdd ouverte")
        session = sessionmaker(bind=engine)()
        yield session

    except Exception as e:
        logger.error(f"An exception has occured: {e}")
        raise e

    finally:
        logger.debug("Closing connection")
        session.close()
        engine.dispose()
        logger.info("Session has been closed.")


def save_to_file(qcm: Qcm, filename: str) -> None:
    """
    Enregistre un qcm dans un fichier

    Args:
        qcm (Qcm): le qcm (rempli) à enregistrer
        filename (str): le chemin du fichier choisi

    Raises:
        Exception (transmission d'exceptions non gérées)
    """

    with open_session(filename) as session:
        try:
            logger.debug("Clearing database...")
            for table_name in inspect(session.bind).get_table_names():
                logger.debug(f"Deleting table {table_name}")
                table = Base.metadata.tables[table_name]
                session.execute(table.delete())
            session.commit()
            logger.debug("Deleted all the tables!")

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

            log_tables(session)

            logger.debug("Writing data to the file")
            session.commit()

            logger.info("Finished writing to file!")
        except Exception as e:
            logger.error(
                f"Failed to write to file because of{e.__class__.__name__} raised: {e}"
            )
            raise e


def read_from_file(filename: str) -> Qcm:
    """
    Ouvre un qcm depuis un fichier

    Args:
        filename (str): le chemin du fichier choisi

    Returns:
        Qcm: le qcm (rempli) lu dans le fichier

    Raises:
        AttributeError: cohérence de la base de données
                        (ne doit contenir qu'un seul Qcm)
        Exception (transmission d'exceptions non gérées)
    """

    with open_session(filename) as session:
        log_tables(session)

        try:
            qcms = session.query(QcmDB).all()
        except Exception as e:
            logger.error(
                f"Failed to read from file because of{e.__class__.__name__} raised: {e}"
            )
            raise e

        if len(qcms) != 1:
            raise AttributeError(f"Expected exactly 1 qcm in the file, got {len(qcms)}")

        db_qcm = qcms[0]
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


def log_tables(session: Session) -> None:
    """
    Logs all the tables of a session and their contents.
    Outputs directly to logger.debug.

    Args:
        session (Session): the open session
    """

    tables = inspect(session.bind).get_table_names()

    logger.debug("Session contents:")
    for table in tables:
        logger.debug(f" - table '{table}'")
        rows = session.execute(text(f"SELECT * FROM {table}")).mappings().all()
        for row in rows:
            logger.debug("   " + str(dict(row)))
