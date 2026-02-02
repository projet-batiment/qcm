# Projet QCM  :

Application graphique permettant de créer, éditer et lancer des questionnaires de différents types. Question à choix multiple, unique et libre. 

Ce projet a été réalisé dans le cadre du module de Développement Collaboratif (INSA Strasbourg).

## Fonctionnalités :

* **Interface graphique** pour ajouter des questions.
* **Types de questions supportés** :
    * Choix Unique.
    * Choix Multiples.
    * Réponse Libre.
* **Gestion des données** : Sauvegarde et chargement des données via une base de données **SQLite** (gérée par SQLAlchemy).

## Installation :

1.  **Cloner le projet** :
    ```
    git clone https://github.com/projet-batiment/qcm.git
    ```

2.  **Installer des packages** :
    ```
    pip install sqlalchemy ttkbootstrap pytest
    ```

## Initialisation de la Base de Données

Avant la première utilisation, vous devez initialiser la base de données locale (`qcm.db`).
Un script est fourni pour initialiser/réinitialiser la BDD.

```
python src/scripts/init_bdd.py
```

## Lancement de l'application :
```
python src/main.py
```

## Auteurs :
- Boré Erwan
- Eich Aurélien
- Poletti Elio
- Régent Gaspard