from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from model.bdd_init import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    enonce = Column(String, nullable=False)
    points = Column(Integer, default=1, nullable=False)
    type_question = Column(String(50))

    qcm_id = Column(Integer, ForeignKey("qcm.id"))
    qcm = relationship("Qcm", back_populates="liste_questions")

    __mapper_args__ = {
        "polymorphic_identity": "question",
        "polymorphic_on": type_question,
    }

    def __init__(self, enonce: str, points: int = 1):
        self.enonce = enonce
        self.points = points


class QuestionQCMultiples(Question):
    __tablename__ = "questions_qcm"
    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    choix_bdd = relationship(
        "Choix",
        order_by="Choix.id",
        collection_class=ordering_list("id"),
        back_populates="question",
        cascade="all, delete-orphan",
    )

    # permet l'édition de la liste sans devoir la réassigner complètement
    choix_rep = association_proxy(
        "choix_bdd",
        "texte",
        creator=lambda texte: Choix(texte=texte, est_correct=False),
    )

    choix_bonne_reponse = association_proxy(
        "choix_bdd",
        "est_correct",
        proxy_factory=set,
        # no creator: only create Choix with choix_rep.append
    )

    __mapper_args__ = {"polymorphic_identity": "qcm_multiple"}

    def __init__(
        self,
        enonce: str,
        points: int,
        choix_rep: List[str] = None,
        id_bonne_reponse: List[int] = None,
    ):
        super().__init__(enonce, points)
        # ici on appel une méthode "choix_rep" qui va créer les objets BDD.
        if choix_rep:
            self.choix_rep = choix_rep
        # ici idem, on indique les bonnes réponses en BDD.
        if id_bonne_reponse:
            self.id_bonne_reponse = id_bonne_reponse

    # Idem pour les bonnes réponses, via les listes
    @property
    def id_bonne_reponse(self) -> set[int]:
        """Trouve les indices des choix marqués 'True' en BDD"""
        indices = set()
        for index, choix in enumerate(self.choix_bdd):
            if choix.est_correct:
                indices.add(index)
        return indices

    @id_bonne_reponse.setter
    def id_bonne_reponse(self, liste_indices: set[int]) -> None:
        """Met à jour les bonnes réponses en BDD via une liste"""
        for index, choix in enumerate(self.choix_bdd):
            if index in liste_indices:
                choix.est_correct = True
            else:
                choix.est_correct = False

    def set_bonne_reponse(self, index: int, value: bool):
        self.choix_bdd[index].est_correct = value

class QuestionQCUnique(QuestionQCMultiples):
    __mapper_args__ = {"polymorphic_identity": "qcm_unique"}

    def __init__(
        self,
        enonce: str,
        points: int,
        choix_rep: List[str] = None,
        id_bonne_reponse: int = -1,
    ):
        """
        :param id_bonne_reponse: Un ENTIER de l'indice correct
        """
        super().__init__(enonce, points, choix_rep, id_bonne_reponse=None)
        # On transforme l'int unique en liste pour le stockage parent
        if id_bonne_reponse >= 0:
            self.id_bonne_reponse = id_bonne_reponse
        else:
            self.id_bonne_reponse = []

    @property
    def id_bonne_reponse(self) -> int:
        """Retourne l'index de la bonne réponse unique."""
        indices = super().id_bonne_reponse
        if len(indices) == 1:
            return next(iter(indices))
        return -1

    @id_bonne_reponse.setter
    def id_bonne_reponse(self, index_correct: int) -> None:
        """Met à jour la bonne réponse unique en BDD."""
        for i, choix in enumerate(self.choix_bdd):
            if i == index_correct:
                choix.est_correct = True
            else:
                choix.est_correct = False


class QuestionLibre(Question):
    __tablename__ = "questions_libre"
    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    rep_attendue = Column(String)
    __mapper_args__ = {"polymorphic_identity": "libre"}

    def __init__(self, enonce: str, points: int, rep_attendue: str):
        super().__init__(enonce, points)
        self.rep_attendue = rep_attendue


# Table pour stocker les choix (car SQL ne gère pas les listes...)
class Choix(Base):
    __tablename__ = "choix"

    id = Column(Integer, primary_key=True, autoincrement=True)
    texte = Column(String, nullable=False)
    est_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions_qcm.id"))
    question = relationship("QuestionQCMultiples", back_populates="choix_bdd")

    def __init__(self, texte: str, est_correct: bool = False):
        self.texte = texte
        self.est_correct = est_correct
