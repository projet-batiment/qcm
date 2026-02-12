from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

import logging

from qcm.db.bdd_init import Base

from qcm.model.qcm import *
from qcm.model.question import *
from qcm.model.reponse import *
from qcm.db.qcm import *
from qcm.db.question import *
from qcm.db.reponse import *

logger = logging.getLogger(__name__)

def open_session(filename: str):
    logger.debug(f"Ouverture du fichier '{filename}'")

    engine = create_engine(
        f"sqlite:///{filename}",
        connect_args={"check_same_thread": False},
        echo=False,
    )

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

    Session = sessionmaker(bind=engine)
    session = Session()
    logger.info("Session de la bdd ouverte")

    return session

def save_to_file(qcm: Qcm, filename: str):
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

            logger.debug("Populating qcm object")
            for question in qcm.liste_questions:
                print_tables(session)

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
                        print_tables(session)

                        db_question.choix_rep = question.choix
                        db_question.id_bonne_reponse = question.index_bonne_reponse
                        session.flush()

                    case QuestionQCMultiples():
                        db_question = QuestionQCMultiplesDB(**arguments)
                        session.add(db_question)
                        session.flush()
                        print_tables(session)

                        db_question.choix_rep = question.choix
                        db_question.id_bonne_reponse = question.index_bonnes_reponses
                        print_tables(session)
                        session.flush()
                        print_tables(session)

                    case QuestionLibre():
                        db_question = QuestionLibreDB(
                            rep_attendue=question.rep_attendue,
                            **arguments,
                        )
                        session.add(db_question)
                        session.flush()

                db_qcm.liste_questions.append(db_question)

                if hasattr(db_question, "choix_bdd"):
                    for each in db_question.choix_bdd:
                        session.add(each)

                session.flush()

            logger.debug("Writing data to the file")
            session.commit()

            logger.info("Finished writing to file!")
        except Exception as e:
            logger.error(f"Failed to write to file because of {e.__class__.__name__} raised: {e}")
            raise e

def print_tables(session):
    tables = inspect(session.bind).get_table_names()
    print("=== TABLES ===")
    for table in tables:
        print(f" {table=}")
        rows = session.execute(text(f"SELECT * FROM {table}")).mappings().all()
        for row in rows:
            print(" > ", dict(row))

def temp_test(filename="/tmp/bdd.dbq"):
    qcm = Qcm(
        liste_questions=[
            QuestionLibre(),
            QuestionQCUnique(choix=["1", "2"]),
            QuestionQCMultiples(choix=["3", "4", "5"], index_bonnes_reponses={0, 1}),
        ]
    )

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"{qcm = }")

    save_to_file(qcm, filename)
