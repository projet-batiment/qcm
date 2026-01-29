from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List
import logging

from src.model.bdd_init import Base
from src.model.qcm import Qcm
from src.model.question import QuestionQCM, QuestionLibre
from src.model.reponse import Reponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BddManager:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///qcm.db", connect_args={"check_same_thread": False}
        )
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Tables vérifiées/créées avec succès.")
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
            logger.error(f"Erreur d'intégrité lors de la sauvegarde : {e}")
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

    def get_qcms(self) -> List[Qcm]:
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
        logger.info("Connexion BDD fermée.")


# tester : python -m src.control.bdd_manager
if __name__ == "__main__":
    import os

    if os.path.exists("qcm.db"):
        os.remove("qcm.db")

    bdd = BddManager()
    r1 = Reponse("4", True)
    r2 = Reponse("2", False)
    q1 = QuestionQCM("2 + 2 ?", 1, [r1, r2])
    q_libre = QuestionLibre("Couleur du cheval blanc ?", 2, "Blanc")
    mon_qcm = Qcm("Test Mixte", [q1, q_libre])
    if bdd.save_qcm(mon_qcm):
        print("Sauvegarde OK")
    # save ok, mtn on teste la récupération
    qcms = bdd.get_qcms()
    for qcm in qcms:
        print(f"\nQCM : {qcm.titre}")
        for q in qcm.liste_questions:
            print(f" - [{q.type_question}] {q.enonce}")
            if isinstance(q, QuestionQCM):
                print(f"   (Choix : {[r.texte for r in q.choix_rep]})")
            elif isinstance(q, QuestionLibre):
                print(f"   (Attendu : {q.rep_attendue})")

    bdd.close_bdd()
