# Guide d'utilisation de la BDD :

Ce document explique comment installer, initialiser et utiliser la base de données SQLite du projet QCM, à l'aide de SQLAlchemy.

## Les indispensables :
sqlalchemy
pytest

## Initialisation de la BDD :
Si vous lancez le projet pour **la premiere** fois, ou si vous voulez remettre la BDD à zéro :

Lancez le script dédié depuis la racine du projet :

``python scripts/init_db.py``

**Résultat :** Un fichier qcm.db est créé à la racine.

## Comment on utilise la BDD (code) :
Toute la logique passe par le BddManager avec SQLAlchemy. On ne manipule jamais de SQL.

Les imports minimum :

```
from src.control.bdd_manager import BddManager
from src.model.qcm import Qcm
from src.model.question import QuestionQCMultiples, QuestionLibre, QuestionQCUnique

bdd = BddManager()
```

## Création et sauvegarde d'un QCM :
Pour créer un QCM, on crée d'abord les questions, puis le QCM, et on sauvegarde le tout.

Une fois les différents objets créés ainsi que l'objet QCM, on fait :

```
q1 = QuestionLibre("Capitale de la France ?", 1, "Paris")

mon_qcm = Qcm("Culture Générale", [q1])

bdd = bdd.save_qcm(mon_qcm)

# bdd étant init par : bdd = BddManager()

```

## Récupération d'un QCM :

``liste_des_qcms = bdd.get_qcms()``

## Supprimer un QCM :
Supposons qu'on veut supprimer le premier de la liste :

```
qcm_a_supprimer = liste_des_qcms[0]

bdd.delete_qcm(qcm_a_supprimer)
```

## Modifier un QCM :
Il suffit de changer les attributs de l'objet Python et de "commit" via la session.

Ex : On change le titre du premier qcm de la liste :

```
qcm = liste_des_qcms[0]
qcm.titre = "Nouveau Titre"
bdd.session.commit()
```

## Lancer les tests
Pour vérifier le bon fonctionnement géneral de la BDD et du model :

``pytest``
