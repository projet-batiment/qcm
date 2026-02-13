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

## Installation et Configuration :

0.  **Pré-requis** :
Avoir Python 3.10 ou supérieur installé.

1.  **Cloner le projet** :
    ```
    git clone https://github.com/projet-batiment/qcm.git
    ```

2.  **Installation standard (Utilisateur)** : Pour installer l'application et ses dépendances
    ```
    pip install .
    ```

3.  **Installation pour le développement** : Pour contribuer au projet :
    ```
    pip install -e ".[dev]"
    ```

    Pour garantir la qualité et le formatage du code, on utilise pre-commit et Ruff.
    ```
    pre-commit install
    ```

## Initialisation de la Base de Données

Avant la première utilisation, vous devez initialiser la base de données locale (`qcm.db`).
Un script est fourni pour initialiser/réinitialiser la BDD.

```
python src/scripts/init_bdd.py
```

## Lancement de l'application :
```
python -m qcm.main
```

## Auteurs :
- Boré Erwan (@bowan71)
- Eich Aurélien (@aeich7)
- Poletti Elio (@LPe7)
- Régent Gaspard (@Gaspard-R)
