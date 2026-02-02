import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from qcm.model.bdd_init import Base
from qcm.model.questionnaire import Qcm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BddManager:
    def __init__(self, db_filename: str = "qcm.db"):
        self.engine = create_engine(
            f"sqlite:///{db_filename}",
            connect_args={"check_same_thread": False},
            echo=False,  # Mettre à True pour voir les requêtes SQL
        )
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Base de données initialisée.")
        except SQLAlchemyError as e:
            logger.critical(f"Impossible de créer les tables : {e}")

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        logger.info("Session de la bdd ouverte")

    def save_qcm(self, qcm_obj: Qcm) -> bool:
        try:
            self.session.add(qcm_obj)
            self.session.commit()
            logger.info(f"QCM '{qcm_obj.titre}' sauvegardé avec succès.")
            return True
        except IntegrityError as e:
            logger.error(
                f"Erreur d'intégrité lors de la sauvegarde "
                f"(ex: id non-unique, à vérifier) : {e}"
            )
            self.session.rollback()
            return False
        except SQLAlchemyError as e:
            logger.error(f"Erreur SQLAlchemy lors de la sauvegarde : {e}")
            self.session.rollback()
            return False
        except Exception as e:
            logger.error(f"Erreur inconnue : {e}")
            self.session.rollback()
            return False

    def get_qcms(self) -> list[Qcm]:
        try:
            return self.session.query(Qcm).all()
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la récupération des QCMs : {e}")
            return []

    def delete_qcm(self, qcm: Qcm) -> bool:
        try:
            self.session.delete(qcm)
            self.session.commit()
            logger.info(f"QCM '{qcm.titre}' supprimé.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Impossible de supprimer le QCM : {e}. On rollback.")
            self.session.rollback()
            return False

    def close_bdd(self) -> None:
        self.session.close()
        self.engine.dispose()
        logger.info("Connexion BDD fermée.")
