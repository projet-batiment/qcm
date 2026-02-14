from contextlib import contextmanager
from logging import getLogger
from typing import ContextManager

from qcm.control.db import model2db, db2model

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from qcm.db.qcm import Base, QcmDB
from qcm.db.tentative import TentativeDB
from qcm.model.data import QcmData

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


def save_to_file(data: QcmData, filename: str) -> None:
    """
    Enregistre un qcm et ses tentatives dans un fichier.
    Vérifie que chaque tentative est reliée au même qcm.

    Args:
        data (QcmData): les données (qcm et tentatives) à enregistrer
        filename (str): le chemin du fichier choisi

    Raises:
        AttributeError: les tentatives ont des qcm différents
        Exception: (transmission d'exceptions non gérées)
    """

    with open_session(filename) as session:
        try:
            # clear the file
            logger.debug("Clearing database...")
            for table_name in inspect(session.bind).get_table_names():
                logger.debug(f"Deleting table {table_name}")
                table = Base.metadata.tables[table_name]
                session.execute(table.delete())
            session.commit()
            logger.debug("Deleted all the tables!")

            # populate the file
            db_qcm = model2db.convert_qcm(session, data.qcm)
            for i, tentative in enumerate(data.tentatives):
                if tentative.qcm != data.qcm:
                    logger.error(f"Expected all references to qcm to"
                                 f" be the same, but tentative #{i}"
                                 f" '{tentative.name}' has a differing one")
                    raise AttributeError(f"Tentative #{i} has differing qcm")

                model2db.convert_tentative(session, tentative, db_qcm)

            # log and write new contents
            log_tables(session)

            logger.debug("Writing data to the file")
            session.commit()

            logger.info("Finished writing to file!")
        except Exception as e:
            logger.error(
                f"Failed to write to file because of"
                f" {e.__class__.__name__} raised: {e}"
            )
            raise e


def read_from_file(filename: str) -> QcmData:
    """
    Ouvre un qcm depuis un fichier

    Args:
        filename (str): le chemin du fichier choisi

    Returns:
        QcmData: le qcm et ses tentatives, lus dans le fichier

    Raises:
        AttributeError: cohérence de la base de données
                        (ne doit contenir qu'un seul Qcm)
        Exception (transmission d'exceptions non gérées)
    """

    with open_session(filename) as session:
        log_tables(session)

        # read and check data consistency
        try:
            qcms = session.query(QcmDB).all()
        except Exception as e:
            logger.error(
                f"Failed to read from file because of{e.__class__.__name__} raised: {e}"
            )
            raise e

        if len(qcms) != 1:
            raise AttributeError(f"Expected exactly 1 qcm in the file, got {len(qcms)}")

        # populate the model
        db_qcm = qcms[0]
        data = QcmData(db2model.convert_qcm(db_qcm))

        for db_tentative in session.query(TentativeDB).all():
            data.tentatives.append(db2model.convert_tentative(db_tentative, data.qcm))

        return data

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
