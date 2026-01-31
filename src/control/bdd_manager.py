from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List
import logging

from src.model.bdd_init import Base
from src.model.qcm import Qcm
from src.model.question import QuestionQCMultiples, QuestionLibre

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BddManager:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///qcm.db",
            connect_args={"check_same_thread": False},
            echo=False,  # Mettre à True pour voir les requêtes SQL
        )
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Base de données initialisée.   ")
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
                f"Erreur d'intégrité lors de la sauvegarde (ex: id non-unique, à vérifier) : {e}"
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

    # test création QCM Multiple
    q_multiple = QuestionQCMultiples(
        enonce="Quels sont les chiffres pairs ?",
        points=1,
        choix_rep=["1", "2", "3", "4"],
        id_bonne_reponse=[1, 3],
    )

    # test création QCM Libre
    q_libre = QuestionLibre(
        enonce="Quelle est la capitale de la France ?", points=2, rep_attendue="Paris"
    )

    # Creéation du qcm
    mon_qcm = Qcm("Test Mixte", [q_multiple, q_libre])
    if bdd.save_qcm(mon_qcm):
        print("Sauvegarde OK")

    # save ok, mtn on teste la récupération
    print("\n Lecture de la BDD :")
    qcms = bdd.get_qcms()
    for qcm in qcms:
        print(f"\nQCM : {qcm.titre}")
        for q in qcm.liste_questions:
            print(f" - [{q.type_question}] {q.enonce}")
            if isinstance(q, QuestionQCMultiples):
                print(f"   Choix : {q.choix_rep}")
                print(f"   Bonnes réponses (indices) : {q.id_bonne_reponse}")
            elif isinstance(q, QuestionLibre):
                print(f"   Réponse attendue : {q.rep_attendue}")

    bdd.close_bdd()
