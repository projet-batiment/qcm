# Projet QCM  :

Application graphique permettant de créer, éditer et lancer des questionnaires de différents types. Question à choix multiple, unique et libre.

Ce projet a été réalisé dans le cadre du module de Développement Collaboratif (INSA Strasbourg).

## Documentation

Pour un mode d'emploi et des informations sur la sauvegard : voir dans le dossier `docs`.

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
    ```sh
    git clone https://github.com/projet-batiment/qcm.git
    ```

2.  **Installation standard (Utilisateur)** : Pour installer l'application et ses dépendances
    ```sh
    pip install .
    ```

3.  **Installation pour le développement** : Pour contribuer au projet :
    ```sh
    pip install -e ".[dev]"
    ```

    Pour garantir la qualité et le formatage du code, on utilise pre-commit et Ruff.
    ```sh
    pre-commit install
    ```

## Lancement de l'application :

```sh
python -m src.qcm
```

## Auteurs :
- Boré Erwan (@bowan71)
- Eich Aurélien (@aeich7)
- Poletti Elio (@LPe7)
- Régent Gaspard (@Gaspard-R)
